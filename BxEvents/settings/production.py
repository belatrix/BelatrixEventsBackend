# settings/production.py
"""
If you use heroku set this constant in your configuration
DJANGO_SETTINGS_MODULE=BxEvents.settings.production
"""

import dj_database_url
from .base import *  # noqa: F403
from utils.environment import env

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY', '')

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases
# Update database configuration with $DATABASE_URL.

db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)  # noqa: F405

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# PUSH NOTIFICATIONS
FIREBASE_SERVER_KEY = env('FIREBASE_SERVER_KEY', '')

# Email
EMAIL_HOST = env('EMAIL_HOST', '')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD', '')
EMAIL_HOST_USER = env('EMAIL_HOST_USER', '')
EMAIL_PORT = env('EMAIL_PORT', '')
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL', '')
