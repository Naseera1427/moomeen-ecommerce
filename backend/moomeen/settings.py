from pathlib import Path
import os

from dotenv import load_dotenv


# =========================================================
# BASE DIRECTORY
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


def env_bool(name, default=False):
    return os.getenv(name, str(default)).lower() in {"1", "true", "yes", "on"}


DEBUG = env_bool("DJANGO_DEBUG")

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")
if not SECRET_KEY:
    if DEBUG:
        SECRET_KEY = "django-insecure-local-development-key"
    else:
        raise RuntimeError("DJANGO_SECRET_KEY must be set when DJANGO_DEBUG is false")

allowed_hosts_env = os.getenv("DJANGO_ALLOWED_HOSTS", "127.0.0.1,localhost")
ALLOWED_HOSTS = [
    host.strip()
    for host in allowed_hosts_env.split(",")
    if host.strip()
]

# Allow Cloudflare Tunnel, ngrok, and test runner
if DEBUG:
    ALLOWED_HOSTS.extend([
        "testserver",
        ".trycloudflare.com",
        ".ngrok-free.app",
        ".ngrok.app",
        ".ngrok.io",
    ])

# Railway deployment domains
ALLOWED_HOSTS.extend([
    ".railway.app",
    ".up.railway.app",
])
if os.getenv("RAILWAY_PUBLIC_DOMAIN"):
    ALLOWED_HOSTS.append(os.getenv("RAILWAY_PUBLIC_DOMAIN"))


# =========================================================
# INSTALLED APPS
# =========================================================

INSTALLED_APPS = [

    # Django built-in apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # MOOMEEN application
    "store",
]


# =========================================================
# MIDDLEWARE
# =========================================================

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",

    "django.middleware.common.CommonMiddleware",

    "django.middleware.csrf.CsrfViewMiddleware",

    "django.contrib.auth.middleware.AuthenticationMiddleware",

    "django.contrib.messages.middleware.MessageMiddleware",

    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# =========================================================
# ROOT URL CONFIGURATION
# =========================================================

ROOT_URLCONF = "moomeen.urls"


# =========================================================
# TEMPLATES
# =========================================================

TEMPLATES = [

    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",

        "DIRS": [],

        "APP_DIRS": True,

        "OPTIONS": {

            "context_processors": [

                "django.template.context_processors.request",

                "django.contrib.auth.context_processors.auth",

                "django.contrib.messages.context_processors.messages",

            ],
        },
    },
]


# =========================================================
# WSGI / ASGI
# =========================================================

WSGI_APPLICATION = "moomeen.wsgi.application"

ASGI_APPLICATION = "moomeen.asgi.application"

# =========================================================
# DATABASE
# =========================================================
database_url = os.getenv("DATABASE_URL")

if database_url:
    try:
        import dj_database_url
        DATABASES = {
            "default": dj_database_url.parse(database_url, conn_max_age=600)
        }
    except ImportError:
        pass
elif os.getenv("POSTGRES_DB"):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.environ["POSTGRES_DB"],
            "USER": os.getenv("POSTGRES_USER", "postgres"),
            "PASSWORD": os.getenv("POSTGRES_PASSWORD", ""),
            "HOST": os.getenv("POSTGRES_HOST", "localhost"),
            "PORT": os.getenv("POSTGRES_PORT", "5432"),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
# =========================================================
# PASSWORD VALIDATION
# =========================================================

AUTH_PASSWORD_VALIDATORS = [

    {
        "NAME":
            "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },

    {
        "NAME":
            "django.contrib.auth.password_validation.MinimumLengthValidator",
    },

    {
        "NAME":
            "django.contrib.auth.password_validation.CommonPasswordValidator",
    },

    {
        "NAME":
            "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# =========================================================
# INTERNATIONALIZATION
# =========================================================

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Kolkata"

USE_I18N = True

USE_TZ = True


# =========================================================
# STATIC FILES
# =========================================================

STATIC_URL = "static/"

STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_DIRS = [
    BASE_DIR / "store" / "static",
]

CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in os.getenv("DJANGO_CSRF_TRUSTED_ORIGINS", "").split(",")
    if origin.strip()
]

# Allow Cloudflare Tunnel and ngrok HTTPS origins for preview testing
if DEBUG:
    CSRF_TRUSTED_ORIGINS.extend([
        "https://*.trycloudflare.com",
        "https://*.ngrok-free.app",
        "https://*.ngrok.app",
        "https://*.ngrok.io",
    ])
    # Tunnel terminates TLS — tell Django the request was originally HTTPS
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Railway deployment HTTPS origins
CSRF_TRUSTED_ORIGINS.extend([
    "https://*.railway.app",
    "https://*.up.railway.app",
])
if os.getenv("RAILWAY_PUBLIC_DOMAIN"):
    railway_domain = os.getenv("RAILWAY_PUBLIC_DOMAIN")
    CSRF_TRUSTED_ORIGINS.append(f"https://{railway_domain}")

if not DEBUG:
    SECURE_SSL_REDIRECT = env_bool("DJANGO_SECURE_SSL_REDIRECT", default=True)
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# =========================================================
# SESSION PERSISTENCE
# =========================================================

# Keep users logged in for 30 days (in seconds)
SESSION_COOKIE_AGE = 60 * 60 * 24 * 30

# Refresh the session expiry on every request so active users
# don't get logged out unexpectedly.
SESSION_SAVE_EVERY_REQUEST = True

# Use database-backed sessions — persists across server restarts.
SESSION_ENGINE = "django.contrib.sessions.backends.db"


# =========================================================
# MEDIA & STORAGES CONFIGURATION
# =========================================================

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"


# =========================================================
# DEFAULT PRIMARY KEY
# =========================================================

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# =========================================================
# AUTHENTICATION
# =========================================================

# When login is required, Django sends the user here.
LOGIN_URL = "login"

# After successful login, go to Home (overridden by ?next= param).
LOGIN_REDIRECT_URL = "home"

# After logout, go to Home.
LOGOUT_REDIRECT_URL = "home"