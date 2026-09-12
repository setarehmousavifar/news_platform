# nevox news!

Bilingual news platform built with Django (English / Persian). Public magazine site, editorial admin desk, REST API with JWT, SEO, and demo seed data.

**Author:** Setare Mousavi  
**Repository:** https://github.com/setarehmousavifar/news_platform.git

---

## Requirements

| Tool | Version |
|------|---------|
| Python | 3.10 – 3.13 |
| MySQL / MariaDB | 8.x / 10.4+ (XAMPP works on Windows) |
| OS | Windows / macOS / Linux |

Optional: Redis, Meilisearch, Docker.

---

## Quick start (Windows / PowerShell)

```powershell
cd news_platform

python -m venv venv
.\venv\Scripts\Activate.ps1

pip install -r requirements.txt

copy .env.example .env
# Edit .env and set DB_PASSWORD to your MySQL password

# In MySQL / phpMyAdmin:
# CREATE DATABASE news_platform CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

python manage.py migrate
python manage.py seed_premium --purge --skip-translate
# Optional Persian article translations (needs internet):
# python manage.py translate_news --force --clear

python manage.py runserver localhost:8000
```

Open:

- Site (EN): http://localhost:8000/
- Site (FA): http://localhost:8000/fa/
- Django admin: http://localhost:8000/admin/
- API docs: http://localhost:8000/api/docs/

### Demo accounts (after seed)

| Role | Username | Password |
|------|----------|----------|
| Super admin | `admin` | `admin1234` (or `SEED_ADMIN_PASSWORD` in `.env`) |
| Journalists | `sarah_chen`, `marcus_webb`, … | `seedpass123` |

If `admin` already exists and the password is unknown:

```powershell
python manage.py shell -c "from accounts.models import CustomUser; u=CustomUser.objects.get(username='admin'); u.set_password('admin1234'); u.user_type='super_admin'; u.save()"
```

---

## If `mysqlclient` fails on Windows

`requirements.txt` includes **PyMySQL**. The project uses it automatically when `mysqlclient` is missing:

```powershell
pip install PyMySQL
```

Then run migrate / runserver again.

---

## Notes

1. Use **`http://localhost:8000/`** (avoid mixing with `127.0.0.1`) so CSRF stays valid.
2. Start **MySQL in XAMPP** before `runserver`.
3. Do not commit `.env` or `venv/`.
4. UI strings use Django i18n (`locale/fa/`). Article Persian text comes from stored `translations` (filled by `translate_news`).
5. `seed_premium` creates about **84 English articles** across **21 categories**, with images and 2 YouTube embeds.

---

## Features

- Home sections: Featured, Trending, Popular, Latest, World, Top stories
- News list, search, category and tag pages
- Bilingual UI (`en` / `fa`) with RTL layout
- Comments, likes, saved stories
- Admin desk: create/edit news, keywords, inline images, video URL
- Soft-delete and roles (`normal` / `admin` / `super_admin`)
- REST API + JWT (`/api/v1/…`, `/api/docs/`)
- SEO: sitemap, robots, Open Graph, JSON-LD
- Optional Redis / Meilisearch via `.env`

---

## Useful commands

```powershell
python manage.py migrate
python manage.py seed_demo
python manage.py seed_premium --purge --skip-translate
python manage.py translate_news --force --clear
python manage.py sync_tags
python manage.py rebuild_search_index
python manage.py collectstatic --noinput
python -m pytest -q
```

Recompile Persian UI catalog:

```powershell
python scripts/compile_i18n.py
```

---

## Project structure

```
accounts/          Users, auth, site settings, dashboard
news/              Articles, categories, tags, API, seeders
interactions/      Comments, likes, saved articles
templates/         HTML templates
static/            CSS, JS, brand images
locale/fa/         Persian UI translations
news_platform/     Settings, URLs, middleware
```

---

## Settings

| Mode | Module |
|------|--------|
| Development (default) | `news_platform.settings` → `dev` |
| Production | `news_platform.settings.prod` |

```powershell
$env:DJANGO_SETTINGS_MODULE="news_platform.settings.prod"
```

---

## Docker (optional)

```bash
docker-compose up --build
```

App: http://localhost:8000 — MySQL on host port **3307**.

---

## Security

- Copy `.env.example` → `.env`; do not share real secrets
- Avoid `#` inside an unquoted `SECRET_KEY`
- Default passwords are for local demo only
- Production: `settings.prod`, HTTPS, strong `SECRET_KEY`

---

## Packaging

Zip the project **without**:

- `venv/`, `.venv/`, `news_platform/Lib/`, `news_platform/Scripts/`
- `.env`
- `__pycache__/`, `.pytest_cache/`
- `media/news_images/`, `media/news_videos/` (large; can re-seed)
- `staticfiles/`

Keep: source code, `static/`, `locale/`, `requirements.txt`, `.env.example`, `README.md`, `INSTALL.txt`.
