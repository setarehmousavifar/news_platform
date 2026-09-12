# Defense checklist — nevox news!

Verify each item on `python manage.py runserver localhost:8000` before your defense.

## 1) Public site

- [ ] Home loads: Featured carousel, Trending, Popular, Latest, World, Top stories
- [ ] `/news/` search, category filter, sort, pagination keep query params
- [ ] News detail: content, categories, keywords, related, views, optional video embed
- [ ] About / Contact show SiteSettings (email, phone, description)
- [ ] Theme toggle day/night survives refresh
- [ ] Skip link on Tab; mobile navbar works
- [ ] Logo uses Permanent Marker for **NEWS!**

## 2) Bilingual (EN / FA)

- [ ] Language switcher EN ↔ فا works without long delay
- [ ] `/fa/` shows RTL layout + Persian UI strings
- [ ] Article titles/content show FA when translations exist in DB
- [ ] Topics menu labels are Persian on `/fa/`

## 3) SEO

- [ ] Meta description + Open Graph on home/article
- [ ] `/sitemap.xml` and `/robots.txt` OK
- [ ] Favicon visible

## 4) Normal user

- [ ] Register / Login / Logout
- [ ] Remember me checkbox visible in night mode
- [ ] Like, comment, reply, saved stories
- [ ] Cannot open create/manage/dashboard
- [ ] Profile update saves

## 5) Admin

- [ ] Dashboard stats; **nevox** logo visible in day mode
- [ ] Create/Edit news: categories + Keywords / tags + image/video + preview
- [ ] Manage own news; soft-delete
- [ ] Cannot manage users

## 6) Super admin

- [ ] Manage all news + users + roles
- [ ] Django admin (`/admin/`): News → keywords + Tags
- [ ] Tag model searchable under News → Tags

## 7) API (optional demo)

- [ ] `/api/docs/` Swagger (title: nevox news! API)
- [ ] JWT at `/api/v1/auth/jwt/`
- [ ] `GET /api/v1/news/`
- [ ] `/health/` OK

## 8) Tests

```bash
python -m pytest -q
```

- [ ] Suite passes (or note known failures)

## Short talking points

1. Django SSR site + DRF `/api/v1/` + JWT + role-based access  
2. Bilingual UX: i18n UI + stored article translations  
3. Editorial desk: keywords, media, dashboard  
4. Demo dataset, SEO, caching, pytest  

## Notes

- Seed passwords are for local demo only  
- Redis / Meilisearch are optional  
- `translate_news` needs internet  
- Prefer `localhost` (do not mix with `127.0.0.1`) for CSRF  
