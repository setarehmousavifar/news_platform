/**
 * Article share and save actions.
 */
document.addEventListener('DOMContentLoaded', function () {
    initArticleShare();
    initArticleSave();
    initReadingProgress();
});

function getCsrfToken() {
    const input = document.querySelector('[name=csrfmiddlewaretoken]');
    return input ? input.value : '';
}

function showArticleToast(message) {
    let container = document.querySelector('.toast-container');
    if (!container) {
        container = document.createElement('div');
        container.className = 'toast-container position-fixed top-0 end-0 p-3';
        document.body.appendChild(container);
    }
    const toast = document.createElement('div');
    toast.className = 'toast align-items-center text-bg-dark border-0 show';
    toast.setAttribute('role', 'alert');
    toast.innerHTML = '<div class="d-flex"><div class="toast-body"></div></div>';
    toast.querySelector('.toast-body').textContent = message;
    container.appendChild(toast);
    setTimeout(function () { toast.remove(); }, 2800);
}

function initArticleShare() {
    const btn = document.querySelector('[data-article-share]');
    if (!btn) return;

    btn.addEventListener('click', async function () {
        const title = btn.dataset.shareTitle || document.title;
        const url = btn.dataset.shareUrl || window.location.href;
        if (navigator.share) {
            try {
                await navigator.share({ title: title, url: url });
                return;
            } catch (err) {
                if (err && err.name === 'AbortError') return;
            }
        }
        try {
            await navigator.clipboard.writeText(url);
            showArticleToast('Link copied to clipboard');
        } catch (err) {
            showArticleToast('Could not share this story');
        }
    });
}

function initArticleSave() {
    const btn = document.querySelector('[data-article-save]');
    if (!btn) return;

    const newsId = btn.dataset.newsId;
    const loginUrl = btn.dataset.loginUrl;
    let busy = false;

    btn.addEventListener('click', async function () {
        if (busy) return;
        busy = true;
        btn.disabled = true;
        try {
            const response = await fetch('/interactions/news/' + newsId + '/save/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCsrfToken(),
                    'Accept': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest',
                },
            });
            if (response.status === 401 || response.status === 403) {
                window.location.href = loginUrl;
                return;
            }
            if (!response.ok) throw new Error('Save failed');
            const data = await response.json();
            btn.classList.toggle('is-active', data.saved);
            btn.setAttribute('aria-pressed', data.saved ? 'true' : 'false');
            const label = btn.querySelector('[data-save-label]');
            if (label) label.textContent = data.saved ? 'Saved' : 'Save';
            showArticleToast(data.saved ? 'Story saved' : 'Removed from saved');
        } catch (err) {
            showArticleToast('Could not save this story');
        } finally {
            busy = false;
            btn.disabled = false;
        }
    });
}

function initReadingProgress() {
    const bar = document.querySelector('[data-reading-progress]');
    const article = document.querySelector('.article-page--editorial');
    if (!bar || !article) return;

    let ticking = false;

    function update() {
        const rect = article.getBoundingClientRect();
        const scrollTop = window.scrollY || document.documentElement.scrollTop;
        const articleTop = scrollTop + rect.top;
        const articleHeight = article.offsetHeight;
        const viewport = window.innerHeight;
        const maxScroll = articleHeight - viewport * 0.35;

        if (maxScroll <= 0) {
            bar.style.width = '0%';
            return;
        }

        const progress = Math.min(1, Math.max(0, (scrollTop - articleTop) / maxScroll));
        bar.style.width = (progress * 100).toFixed(2) + '%';
        ticking = false;
    }

    function onScroll() {
        if (!ticking) {
            ticking = true;
            requestAnimationFrame(update);
        }
    }

    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', onScroll, { passive: true });
    update();
}
