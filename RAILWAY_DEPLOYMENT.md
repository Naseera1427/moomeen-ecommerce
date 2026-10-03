# MOOMEEN PRODUCTS — Railway Deployment Guide

This guide explains how to deploy the MOOMEEN PRODUCTS Django application to [Railway](https://railway.app) smoothly and reliably.

---

## 🏗️ Architecture & Deployment Overview

- **Framework**: Django 6.1.1 + Python 3.14 / 3.12+
- **WSGI Server**: Gunicorn
- **Static Files**: WhiteNoise (`CompressedManifestStaticFilesStorage`)
- **Database**: PostgreSQL (provided automatically by Railway via `DATABASE_URL`)
- **Configuration**: `Procfile` and `railway.json` are pre-configured at root and inside `backend/`

---

## 🚀 Step-by-Step Railway Deployment

### Step 1: Create a Railway Project
1. Log in to [Railway](https://railway.app/).
2. Click **+ New Project** → **Deploy from GitHub repo**.
3. Select your repository: `moomeen-ecommerce`.

### Step 2: Add a PostgreSQL Database Service
1. In your Railway project canvas, click **+ Create** → **Database** → **Add PostgreSQL**.
2. Railway will automatically provision a managed PostgreSQL database and create a `DATABASE_URL` variable.

### Step 3: Configure Environment Variables
In your web service settings, go to the **Variables** tab and add:

| Variable | Recommended Value | Notes |
| :--- | :--- | :--- |
| `DJANGO_DEBUG` | `False` | Disables debug mode for security |
| `DJANGO_SECRET_KEY` | *(Generate a 50+ char random string)* | Required in production |
| `DATABASE_URL` | `${{Postgres.DATABASE_URL}}` | Reference your Railway Postgres service |
| `DJANGO_ALLOWED_HOSTS` | `127.0.0.1,localhost` | `.railway.app` is already auto-allowed |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | `https://your-custom-domain.com` | `https://*.railway.app` is already auto-allowed |
| `DJANGO_SECURE_SSL_REDIRECT` | `True` | Forces HTTPS traffic |

*(Note: Railway automatically assigns the `PORT` variable, and Gunicorn is configured to bind to `0.0.0.0:$PORT`.)*

### Step 4: Verify Root Directory / Start Command
Railway automatically detects Python via `requirements.txt` and `railway.json`.
The pre-configured start command automatically runs migrations and static collection on each deployment:
```bash
python manage.py migrate && python manage.py collectstatic --noinput && gunicorn moomeen.wsgi:application --bind 0.0.0.0:$PORT
```

### Step 5: Generate Public Domain
1. In your web service settings, go to **Settings** → **Networking** → **Public Networking**.
2. Click **Generate Domain** (e.g. `moomeen-ecommerce-production.up.railway.app`).

### Step 6: Create Admin User on Railway
Once the deployment status turns green:
1. Open the Railway web terminal (or use Railway CLI: `railway run`):
2. Run the secure setup command:
   ```bash
   python backend/manage.py setup_admin
   ```
   Or if Root Directory is `backend`:
   ```bash
   python manage.py setup_admin
   ```
3. Enter your desired admin username, email, and password.
4. Log in at `https://your-domain.up.railway.app/admin-login/` or `/admin/`.

---

## 💻 Local Development Access

- **Storefront URL**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Admin Login URL**: [http://127.0.0.1:8000/admin-login/](http://127.0.0.1:8000/admin-login/)
- **Admin Dashboard**: [http://127.0.0.1:8000/admin-dashboard/](http://127.0.0.1:8000/admin-dashboard/)
- **Django Admin**: [http://127.0.0.1:8000/django-admin/](http://127.0.0.1:8000/django-admin/)
