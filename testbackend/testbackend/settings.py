from pathlib import Path

from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = (
    "django-insecure-*$c!r(^j9dq0mt#lpgec8ho7k2k*@wy0i416!^oqigmu%!av=e"
)

DEBUG = True

USE_S3 = config("USE_S3", default=False, cast=bool)

ALLOWED_HOSTS = ["127.0.0.1", "localhost", "*"]

INSTALLED_APPS = [
    "daphne",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "storages",
    "projectsAPI.apps.ProjectsapiConfig",
    "imagesAPI.apps.ImagesapiConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "testbackend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",
    },
}


ASGI_APPLICATION = "testbackend.asgi.application"

if USE_S3:
    AWS_ACCESS_KEY_ID = config("S3_KEY_ID", cast=str)
    AWS_SECRET_ACCESS_KEY = config("S3_SECRET_ACCESS_KEY", cast=str)
    AWS_STORAGE_BUCKET_NAME = config("S3_BUCKET_NAME", cast=str)
    AWS_S3_ENDPOINT_URL = config("S3_HOST", cast=str)
    MEDIA_URL = f"{AWS_S3_ENDPOINT_URL}/media/"
    DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
    STATICFILES_STORAGE = "testbackend.storage.StaticRootS3BotoStorage"
else:
    DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"
    MEDIA_URL = "/media/"
    MEDIA_ROOT = BASE_DIR / "media"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    },
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib."
        "auth.password_validation."
        "UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth."
        "password_validation."
        "MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth."
        "password_validation."
        "CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth."
        "password_validation."
        "NumericPasswordValidator",
    },
]


LANGUAGE_CODE = "ru"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_URL = "static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
