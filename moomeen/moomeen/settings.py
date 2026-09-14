from pathlib import Path
import os


# =========================================================
# BASE DIRECTORY
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent


# =========================================================
# SECRET KEY
# =========================================================

SECRET_KEY = os.getenv(
    "DJANGO_SECRET_KEY",
    "django-insecure-moomeen-local-development-key"
)


# =========================================================
# DEVELOPMENT MODE
# =========================================================

DEBUG = True


# =========================================================
# ALLOWED HOSTS
# =========================================================

ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
]


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
# PostgreSQL
# =========================================================
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "moomeen",
        "USER": "postgres",
        "PASSWORD": os.getenv(
            "POSTGRES_PASSWORD",
            "Fharook@123"
        ),
        "HOST": "localhost",
        "PORT": "5432",
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

STATICFILES_DIRS = [
    BASE_DIR / "store" / "static",
]


# =========================================================
# MEDIA FILES
# =========================================================

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

# After successful login, go to Home.
LOGIN_REDIRECT_URL = "home"

# After logout, go to Home.
LOGOUT_REDIRECT_URL = "home"