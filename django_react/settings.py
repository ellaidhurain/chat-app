"""
Django settings for django_react project.

Generated by 'django-admin startproject' using Django 3.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "o5x_ev&d$v1*6#vgm=u-_q7m$v2vm58@gr&544_3k(vx59^_en"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "api",
    "frontend",
    "rest_framework.authtoken",
    "channels",
    # 'django_extensions',
    "oauth2_provider",
    "social_django",
    "corsheaders",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",  # cors resolving middleware
    
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",  # This middleware is responsible for generating and verifying CSRF tokens.
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "oauth2_provider.middleware.OAuth2TokenMiddleware",  # oauth token middleware
]

ROOT_URLCONF = "django_react.urls"

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

WSGI_APPLICATION = "django_react.wsgi.application"

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

import dj_database_url

DATABASE_URL = "mysql://root:MhpYFGvac0Ze4b5F7IOG@containers-us-west-146.railway.app:7539/railway"

DATABASES = {
    "default": dj_database_url.config(default=DATABASE_URL, conn_max_age=1800),
    }


# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.mysql",
#         "NAME": "chat",
#         "USER": "root",
#         "PASSWORD": "EllaiDhurai007",
#         "HOST": "localhost",
#         "PORT": "3306",
#         "OPTIONS": {
#             "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
#         },
#     },
# }

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

import os

# to store uploaded media files(images,videos,files)
MEDIA_ROOT = os.path.join(BASE_DIR, "static/files")
MEDIA_URL = "/files/"


STATIC_URL = "/static/"
# collect static files from static directory in development
STATICFILES_DIRS = [os.path.join(BASE_DIR, "frontend/static")]

# static root is used to copy all static files from staticfiles_dirs in production.
# to execute this we need to use django collectstatic
# This directory is typically served by a web server in production.
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

# python manage.py collectstatic

# This command is useful when you're deploying your Django project to a
# production environment and you want to collect all your static files in a
# single directory. By doing this, you can serve your static files using a
# web server like Nginx or Apache,
# which is typically faster and more efficient than serving them through Django.
# we need to run the collectstatic command every time you add or modify a static file
# in your project, so that the changes are reflected in the STATIC_ROOT directory.


DISABLE_COLLECTSTATIC = 0

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",
        "oauth2_provider.contrib.rest_framework.OAuth2Authentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        # 'rest_framework.permissions.IsAuthenticated',
    ],
}

AUTHENTICATION_BACKENDS = [
    # 'social_core.backends.google.GoogleOAuth2',
    "django.contrib.auth.backends.ModelBackend",
    "oauth2_provider.backends.OAuth2Backend",
]


OAUTH2_PROVIDER = {
    "ACCESS_TOKEN_EXPIRE_SECONDS": 3600,
    "AUTHORIZATION_CODE_EXPIRE_SECONDS": 60,
    "ALLOWED_REDIRECT_URI_SCHEMES": ["http", "https"],
    "REFRESH_TOKEN_EXPIRE_SECONDS": 300,
    "REQUEST_APPROVAL_PROMPT": "auto",
    "ROTATE_REFRESH_TOKENS": True,
    "SCOPES": {
        "read": "Read scope",
        "write": "Write scope",
    },
}


OAUTH_ACCESS_TOKEN_MODEL = "oauth2_provider.models.AccessToken"

# cookie
TOKEN_COOKIE_NAME = "token"
TOKEN_EXPIRATION_TIME = 3600  # seconds
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_SAMESITE = "Strict"


SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = (
    "1045824655965-bvcoqigok9ov035oaaditpp0gs7rmmp3.apps.googleusercontent.com"
)
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = "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"
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
    "profile",
    "email",
]

LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "/"
# http://localhost:8000/oauth2callback/

AUTH_USER_MODEL = "auth.User"

ASGI_APPLICATION = "django_react.routing.application"


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "": {
            "handlers": ["console"],
            "level": "DEBUG",
        },
        "oauthlib": {
            "level": "WARNING",
        },
    },
}


CLIENT_ID = "bdmW3Kbs0fUDPLTO0kGbamLUsg0qmRLA45pG7Hz5"
CLIENT_SECRET = "OELQWJsqojUKyryxS98Kf1kYvBjNCEmqJIrn5DDUVSQk5nvYgkBYf0bA6L81ZPWkpco3qsAQK08EGh2IQxJ9dsR2gtG4TWLJv7NETMKvyI6RmIoRA7vbBdz9Sl3OvK8o"


# CLIENT_ID = "YV49s60WC2RutKU8L1itISqFGfmOoMdQVt7nX5jp"
# CLIENT_SECRET = "XqKC6p3rQPuOkAFb83ltzWIZyZgx2T5GOe6ITEK2BCWDjLCo5zBRtxoa5ydR3RcB8bnvmDetU8nc9dG6MFhlMZ3tYPubGUi4iVVq5SHS7woTPqBLRrurfHKpZniLmoEW"


# CORS_ALLOWED_ORIGINS = [
#     "http://localhost:3000",
# ]


CORS_ORIGIN_ALLOW_ALL = True
