"""Auto-translation for news content (EN ↔ FA) with DB persistence."""

from __future__ import annotations

import hashlib
import logging
import re
import time

from django.core.cache import cache
from django.utils import translation

from deep_translator import GoogleTranslator

logger = logging.getLogger(__name__)

PERSIAN_RE = re.compile(r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF]')
CACHE_TTL = 60 * 60 * 24 * 7
CHUNK_SIZE = 4500
MAX_RETRIES = 3


def is_persian_text(value: str) -> bool:
    return bool(PERSIAN_RE.search(str(value or '')))


def source_language(news) -> str:
    title = getattr(news, 'title', '') or ''
    content = getattr(news, 'content', '') or ''
    if is_persian_text(title) or is_persian_text(content[:500]):
        return 'fa'
    return 'en'


def _cache_key(text: str, target: str, source: str) -> str:
    digest = hashlib.md5(f'{source}:{target}:{text}'.encode('utf-8')).hexdigest()
    return f'nevox_tr:{digest}'


def _is_valid_translation(original: str, translated: str, target: str) -> bool:
    original = (original or '').strip()
    translated = (translated or '').strip()
    if not translated or translated == original:
        return False
    if target == 'fa':
        return is_persian_text(translated)
    if target == 'en' and is_persian_text(original):
        return not is_persian_text(translated)
    return True


def translate_text(text: str, target: str, source: str | None = None) -> str:
    text = (text or '').strip()
    if not text:
        return ''
    src = source or ('fa' if is_persian_text(text) else 'en')
    if src == target:
        return text

    key = _cache_key(text, target, src)
    cached = cache.get(key)
    if cached is not None and _is_valid_translation(text, cached, target):
        return cached

    last_exc = None
    for attempt in range(MAX_RETRIES):
        try:
            translator = GoogleTranslator(source=src, target=target)
            if len(text) <= CHUNK_SIZE:
                result = (translator.translate(text) or '').strip()
            else:
                parts = []
                for para in text.split('\n\n'):
                    chunk = (para or '').strip()
                    if not chunk:
                        parts.append('')
                        continue
                    if len(chunk) > CHUNK_SIZE:
                        sentences = re.split(r'(?<=[.!?])\s+', chunk)
                        buf = ''
                        for sentence in sentences:
                            if len(buf) + len(sentence) > CHUNK_SIZE and buf:
                                parts.append(translator.translate(buf.strip()))
                                buf = sentence
                            else:
                                buf = f'{buf} {sentence}'.strip()
                        if buf:
                            parts.append(translator.translate(buf))
                    else:
                        parts.append(translator.translate(chunk))
                result = '\n\n'.join(parts).strip()
            if result and _is_valid_translation(text, result, target):
                cache.set(key, result, CACHE_TTL)
                return result
        except Exception as exc:
            last_exc = exc
            if attempt < MAX_RETRIES - 1:
                time.sleep(0.6 * (attempt + 1))
    if last_exc:
        logger.warning('Translation failed (%s → %s): %s', src, target, last_exc)
    return text


def _persist_translation(news, lang: str, field: str, value: str) -> None:
    translations = dict(news.translations or {})
    bucket = dict(translations.get(lang) or {})
    bucket[field] = value
    translations[lang] = bucket
    news.translations = translations
    news.save(update_fields=['translations'])


def ensure_news_translations(news, *, force: bool = False) -> dict:
    """Populate news.translations for the opposite language."""
    src = source_language(news)
    target = 'fa' if src == 'en' else 'en'
    translations = dict(news.translations or {})
    bucket = dict(translations.get(target) or {})

    if force or not _is_valid_translation(news.title, bucket.get('title', ''), target):
        title_tr = translate_text(news.title, target=target, source=src)
        if _is_valid_translation(news.title, title_tr, target):
            bucket['title'] = title_tr

    if force or not _is_valid_translation((news.content or '')[:300], (bucket.get('content') or '')[:500], target):
        content_tr = translate_text(news.content, target=target, source=src)
        if _is_valid_translation((news.content or '')[:300], content_tr[:500] if content_tr else '', target):
            bucket['content'] = content_tr

    if bucket:
        translations[target] = bucket
    elif target in translations:
        translations.pop(target, None)

    if translations != (news.translations or {}):
        news.translations = translations
        news.save(update_fields=['translations'])
    return translations


def get_localized_field(news, field: str, lang: str | None = None) -> str:
    """Return title or content in the requested language (DB/cache only — no live API)."""
    lang = lang or translation.get_language() or 'en'
    lang = lang.split('-')[0]
    original = getattr(news, field, '') or ''
    src = source_language(news)

    cache_attr = f'_loc_{lang}_{field}'
    memo = getattr(news, cache_attr, None)
    if memo is not None:
        return memo

    if lang == src:
        setattr(news, cache_attr, original)
        return original

    bucket = (news.translations or {}).get(lang) or {}
    stored = bucket.get(field) or ''
    if _is_valid_translation(original, stored, lang):
        setattr(news, cache_attr, stored)
        return stored

    setattr(news, cache_attr, original)
    return original


def get_cached_text_translation(text: str, target: str, source: str | None = None) -> str:
    """Return a cached translation if available; otherwise try live translate."""
    text = (text or '').strip()
    if not text:
        return ''
    src = source or ('fa' if is_persian_text(text) else 'en')
    if src == target:
        return text
    cached = cache.get(_cache_key(text, target, src))
    if cached and _is_valid_translation(text, cached, target):
        return cached
    translated = translate_text(text, target=target, source=src)
    if _is_valid_translation(text, translated, target):
        return translated
    return text


def get_localized_category_name(category, lang: str | None = None) -> str:
    from .category_labels import get_category_label

    lang = lang or translation.get_language() or 'en'
    lang = lang.split('-')[0]
    return get_category_label(category.name, lang)


def clear_invalid_translations(news) -> bool:
    """Remove stored translations that are identical to the source text."""
    translations = dict(news.translations or {})
    changed = False
    src = source_language(news)
    target = 'fa' if src == 'en' else 'en'
    bucket = dict(translations.get(target) or {})
    for field in ('title', 'content'):
        original = getattr(news, field, '') or ''
        stored = bucket.get(field, '')
        if stored and not _is_valid_translation(original, stored, target):
            bucket.pop(field, None)
            changed = True
    if bucket:
        translations[target] = bucket
    elif target in translations:
        translations.pop(target)
        changed = True
    if changed:
        news.translations = translations
        news.save(update_fields=['translations'])
    return changed
