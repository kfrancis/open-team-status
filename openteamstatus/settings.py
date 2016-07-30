from __future__ import absolute_import
"""
Django settings for openteamstatus project.

Generated by 'django-admin startproject' using Django 1.9.8.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os

from django.core.urlresolvers import reverse_lazy
from celery.schedules import crontab

def env_setting(var, default=None, type=lambda x: x):
    globals()[var] = type(os.environ.get(var, default))

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
env_setting('SECRET_KEY', '+iwwd*@_y@2=0#6_&4e7)#hvdc)7mw)%g(xbk62zg-b%h0$dc6')

# SECURITY WARNING: don't run with debug turned on in production!
env_setting('DEBUG', default='true', type=lambda x: x.lower() == 'true')

env_setting('ALLOWED_HOSTS', default='', type=lambda x: x.split(':'))


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    'django_markdown2',
    'djcelery',
    'kombu.transport.django',

    'core',
    'checkins',
    'magiclink',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'whitenoise.middleware.WhiteNoiseMiddleware',

    'core.middeware.OpenTeamStatusSettingsMiddleware',
]

ROOT_URLCONF = 'openteamstatus.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'openteamstatus.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {}
import dj_database_url

DATABASES['default'] = dj_database_url.config(default='sqlite:///db.sqlite3')


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

env_setting('TIME_ZONE', default='UTC')

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

LOGIN_URL = reverse_lazy('login')
LOGIN_REDIRECT_URL = '/'

SITE_ID = 1

env_setting('EMAIL_HOST')
env_setting('EMAIL_PORT', default=25, type=int)
env_setting('EMAIL_HOST_PASSWORD')
env_setting('EMAIL_HOST_USER')
env_setting('EMAIL_SUBJECT_PREFIX', default='[OpenTeamStatus]')
env_setting('EMAIL_USE_TLS', default='false',
            type=lambda x: x.lower() == 'true')
env_setting('EMAIL_USE_SSL', default='false',
            type=lambda x: x.lower() == 'true')
env_setting('EMAIL_SSL_CERTFILE')
env_setting('EMAIL_SSL_KEYFILE')
env_setting('EMAIL_TIMEOUT')
env_setting('DEFAULT_FROM_EMAIL', default='openteamstatus@localhost')

CELERY_RESULT_BACKEND = 'djcelery.backends.database:DatabaseBackend'
BROKER_URL = 'django://'

env_setting('OPEN_TEAM_STATUS_NAME', default='Open Team Status')
env_setting('OPEN_TEAM_STATUS_LOGO')
env_setting('OPEN_TEAM_STATUS_SLACK_WEBHOOK')
env_setting('OPEN_TEAM_STATUS_REMINDER_HOUR', default=9, type=int)
env_setting('OPEN_TEAM_STATUS_REMINDER_MINUTE', default=0, type=int)
env_setting('OPEN_TEAM_STATUS_REMINDER_DAYS', default='mon,tue,wed,thu,fri')
env_setting('OPEN_TEAM_STATUS_REMINDER_SUBJECT',
            default='Status Checkin Reminder')
env_setting('OPEN_TEAM_STATUS_REMINDER_BODY',
            default='Please checkin today: {url}')
env_setting('OPEN_TEAM_STATUS_REMINDER_TASK',
            default='checkins.tasks.email_reminder'),
env_setting('OPEN_TEAM_STATUS_REPORT_TASK',
            default='checkins.tasks.email_report'),
env_setting('OPEN_TEAM_STATUS_REPORT_SLACK_CHANNEL', default='#general')
env_setting('OPEN_TEAM_STATUS_REPORT_HOUR', default=12, type=int)
env_setting('OPEN_TEAM_STATUS_REPORT_MINUTE', default=0, type=int)
env_setting('OPEN_TEAM_STATUS_REPORT_DAYS', default='mon,tue,wed,thu,fri')
env_setting('OPEN_TEAM_STATUS_REPORT_SUBJECT', default='Team Status Update')
env_setting('OPEN_TEAM_STATUS_REPORT_BODY', default="""{url}
{checked_in}/{total} users checked in today.
{goals_met}/{total} users met their goals yesterday.
{blocked}/{total} users are blocked today.
""")
env_setting('OPEN_TEAM_STATUS_PUBLIC', 'false', lambda x: x.lower() == 'true')


CELERYBEAT_SCHEDULE = {
    'send-reminder': {
        'task': OPEN_TEAM_STATUS_REMINDER_TASK,
        'schedule': crontab(
            minute=OPEN_TEAM_STATUS_REMINDER_MINUTE,
            day_of_week=OPEN_TEAM_STATUS_REMINDER_DAYS,
            hour=OPEN_TEAM_STATUS_REMINDER_HOUR,
        ),
    },
    'send-report': {
        'task': OPEN_TEAM_STATUS_REPORT_TASK,
        'schedule': crontab(
            minute=OPEN_TEAM_STATUS_REPORT_MINUTE,
            day_of_week=OPEN_TEAM_STATUS_REPORT_DAYS,
            hour=OPEN_TEAM_STATUS_REPORT_HOUR,
        ),
    },
}

if 'DYNO' in os.environ:
    CELERYBEAT_SCHEDULE['heroku-keep-alive'] = {
        'task': 'core.tasks.heroku_keepalive',
        'schedule': crontab(minute='0,15,30,45'),
    }
