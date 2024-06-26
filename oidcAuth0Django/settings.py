"""
Django settings for oidcAuth0Django project.

Generated by 'django-admin startproject' using Django 4.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os
import requests

from dotenv import load_dotenv, find_dotenv
import logging

# Set up logging
LOGGER = logging.getLogger(__name__)

# Load environment definition file
ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = BASE_DIR / "templates"

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-qc!jx-b&u1bf*mm^*nez9hl3tc*%xisn)vob$j7uds7mm6a84b"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

AUTH_USER_MODEL = "users.User"
AUTHENTICATION_BACKENDS = ["oidcAuth0Django.backends.PermissionBackend"]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "mozilla_django_oidc",
    "rest_framework",
    "users",
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

ROOT_URLCONF = "oidcAuth0Django.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [TEMPLATE_DIR],
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

WSGI_APPLICATION = "oidcAuth0Django.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "mozilla_django_oidc.contrib.drf.OIDCAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
}


def discover_oidc(discovery_url: str) -> dict:
    """
    Performs OpenID Connect discovery to retrieve the provider configuration.
    """
    response = requests.get(discovery_url)
    logging.info(f"OpenID Connect discovery response: {response.json()}")
    if response.status_code != 200:
        raise ValueError("Failed to retrieve provider configuration.")

    provider_config = response.json()

    # Extract endpoint URLs from provider configuration
    return {
        "authorization_endpoint": provider_config["authorization_endpoint"],
        "token_endpoint": provider_config["token_endpoint"],
        "userinfo_endpoint": provider_config["userinfo_endpoint"],
        "jwks_uri": provider_config["jwks_uri"],
    }


# OpenID Connect settings
OIDC_RP_CLIENT_ID = os.environ.get("AUTH0_CLIENT_ID")
OIDC_RP_CLIENT_SECRET = os.environ.get("AUTH0_CLIENT_SECRET")
OIDC_OP_BASE_URL = os.environ.get("AUTH0_DOMAIN")

OIDC_RP_SIGN_ALGO = "RS256"
OIDC_RP_SCOPES = "openid profile email"
OIDC_OP_DISCOVERY_ENDPOINT = OIDC_OP_BASE_URL + "/.well-known/openid-configuration"

# Discover OpenID Connect endpoints
discovery_info = discover_oidc(OIDC_OP_DISCOVERY_ENDPOINT)
OIDC_OP_AUTHORIZATION_ENDPOINT = discovery_info["authorization_endpoint"]
OIDC_OP_TOKEN_ENDPOINT = discovery_info["token_endpoint"]
OIDC_OP_USER_ENDPOINT = discovery_info["userinfo_endpoint"]
OIDC_OP_JWKS_ENDPOINT = discovery_info["jwks_uri"]

LOGIN_REDIRECT_URL = "http://127.0.0.1:8000/admin"
LOGOUT_REDIRECT_URL = "http://127.0.0.1:8000/admin"
LOGIN_URL = "http://127.0.0.1:8000/oidc/authenticate/"
