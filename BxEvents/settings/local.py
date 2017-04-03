# settings/local.py
"""
If you use virtualenvwrapper add this line to your postactivate script
export DJANGO_SETTINGS_MODULE=BxEvents.settings.local
"""

from .base import *  # noqa: F403

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '33@^f0=57@&!z&5qy=u876rf5@9&i7$74ar6af^v%gxlq130sd'

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),  # noqa: F405
    }
}
