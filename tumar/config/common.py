import os
from distutils.util import strtobool
from os.path import join

import dj_database_url
from configurations import Configuration
from django.utils.translation import gettext_lazy as _

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Common(Configuration):
    INSTALLED_APPS = (
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'django.contrib.gis',  # geodjango support

        # Third party apps
        'rest_framework',  # utilities for rest apis
        'rest_framework_gis',
        'rest_framework.authtoken',  # token authentication
        'django_filters',  # for filtering rest endpoints
        'rest_auth',

        # Registration related
        'django.contrib.sites',
        'allauth',
        'allauth.account',
        'rest_auth.registration',
        'phone_verify',

        # Social Auth
        'allauth.socialaccount',
        'allauth.socialaccount.providers.facebook',
        'allauth.socialaccount.providers.google',

        # Your apps
        'tumar.users.apps.UsersConfig',
        'tumar.animals.apps.AnimalsConfig',
        'tumar.indicators.apps.IndicatorsConfig',
        'tumar.ecalendar.apps.EcalendarConfig',
    )

    # https://docs.djangoproject.com/en/2.0/topics/http/middleware/
    MIDDLEWARE = (
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.locale.LocaleMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    )

    ALLOWED_HOSTS = ["*"]
    ROOT_URLCONF = 'tumar.urls'
    SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')
    WSGI_APPLICATION = 'tumar.wsgi.application'

    # Email
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

    ADMINS = (
        ('Author', 'epmek96@gmail.com'),
    )

    # Postgres
    DATABASES = {
        'default': dj_database_url.config(
            default='postgis://postgres:01470258@postgres:5432/postgres',
            conn_max_age=int(os.getenv('POSTGRES_CONN_MAX_AGE', 600))
        ),
        'egistic_2': dj_database_url.config(
            default='postgis://docker:docker@94.247.135.91:8086/egistic_2.0',
            conn_max_age=int(os.getenv('POSTGRES_CONN_MAX_AGE', 600))
        )
    }
    # DATABASES['default']['ENGINE'] = 'django.contrib.gis.db.backends.postgis'

    # General
    APPEND_SLASH = False
    TIME_ZONE = 'Asia/Almaty'
    LANGUAGE_CODE = 'ru'
    LANGUAGES = [
        ('en', _('English')),
        ('ru', _('Russian')),
    ]
    SITE_ROOT = os.path.dirname(os.path.realpath(__name__))
    LOCALE_PATHS = [os.path.join(SITE_ROOT, 'locale')]

    # If you set this to False, Django will make some optimizations so as not
    # to load the internationalization machinery.
    USE_I18N = True
    USE_L10N = True
    USE_TZ = True
    LOGIN_REDIRECT_URL = '/'

    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/2.0/howto/static-files/
    STATIC_ROOT = os.path.normpath(join(os.path.dirname(BASE_DIR), 'static'))
    STATICFILES_DIRS = []
    STATIC_URL = '/static/'
    STATICFILES_FINDERS = (
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    )

    # Media files
    MEDIA_ROOT = join(os.path.dirname(BASE_DIR), 'media')
    MEDIA_URL = '/media/'

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': STATICFILES_DIRS,
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

    # Set DEBUG to False as a default for safety
    # https://docs.djangoproject.com/en/dev/ref/settings/#debug
    DEBUG = strtobool(os.getenv('DJANGO_DEBUG', 'no'))

    # Password Validation
    # https://docs.djangoproject.com/en/2.0/topics/auth/passwords/#module-django.contrib.auth.password_validation
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

    # Logging
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'django.server': {
                '()': 'django.utils.log.ServerFormatter',
                'format': '[%(server_time)s] %(message)s',
            },
            'verbose': {
                'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
            },
            'simple': {
                'format': '%(levelname)s %(message)s'
            },
        },
        'filters': {
            'require_debug_true': {
                '()': 'django.utils.log.RequireDebugTrue',
            },
        },
        'handlers': {
            'django.server': {
                'level': 'INFO',
                'class': 'logging.StreamHandler',
                'formatter': 'django.server',
            },
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'simple'
            },
            'mail_admins': {
                'level': 'ERROR',
                'class': 'django.utils.log.AdminEmailHandler'
            }
        },
        'loggers': {
            'django': {
                'handlers': ['console'],
                'propagate': True,
            },
            'django.server': {
                'handlers': ['django.server'],
                'level': 'INFO',
                'propagate': False,
            },
            'django.request': {
                'handlers': ['mail_admins', 'console'],
                'level': 'ERROR',
                'propagate': False,
            },
            'django.db.backends': {
                'handlers': ['console'],
                'level': 'INFO'
            },
        }
    }

    # Custom user app
    AUTH_USER_MODEL = 'users.User'

    # Django Rest Framework
    REST_FRAMEWORK = {
        'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
        'PAGE_SIZE': int(os.getenv('DJANGO_PAGINATION_LIMIT', 30)),
        'DATETIME_FORMAT': '%Y-%m-%dT%H:%M:%S%z',
        'DEFAULT_RENDERER_CLASSES': (
            'rest_framework.renderers.JSONRenderer',
            'rest_framework.renderers.BrowsableAPIRenderer',
        ),
        'DEFAULT_PERMISSION_CLASSES': [
            'rest_framework.permissions.IsAuthenticated',
        ],
        'DEFAULT_AUTHENTICATION_CLASSES': (
            # 'rest_framework.authentication.SessionAuthentication',
            'rest_framework.authentication.TokenAuthentication',
        )
    }

    # django-rest-auth
    SITE_ID = 1
    OLD_PASSWORD_FIELD_ENABLED = True
    LOGOUT_ON_PASSWORD_CHANGE = False

    # ACCOUNT_EMAIL_REQUIRED = True
    # ACCOUNT_UNIQUE_EMAIL = True
    # ACCOUNT_USERNAME_REQUIRED = False
    # USER_MODEL_USERNAME_FIELD = None
    USERNAME_VALIDATORS = ['tumar.users.models.main_validator', ]
    ACCOUNT_ADAPTER = 'tumar.users.adapter.MyAccountAdapter'

    # Add settings for phone_verify to work
    PHONE_VERIFICATION = {
        "BACKEND": "phone_verify.backends.twilio.TwilioBackend",
        "OPTIONS": {
            "SID": "fake",
            "SECRET": "fake",
            "FROM": "+14755292729",
            "SANDBOX_TOKEN": "123456",
        },
        "TOKEN_LENGTH": 6,
        "MESSAGE": "Welcome to {app}! Please use security code {security_code} to proceed.",
        "APP_NAME": "Tumar",
        "SECURITY_CODE_EXPIRATION_TIME": 3600,  # In seconds only
        "VERIFY_SECURITY_CODE_ONLY_ONCE": False,
        # If False, then a security code can be used multiple times for verification
    }
