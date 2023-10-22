# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import os, environ, openai, sys
import logging



def search_in_environment_or_docker_secrets(key : str) -> str:
    result = ""
    try:
        return os.environ[key]
    except KeyError:
        print("Key " + key + " not found in environment variables. Trying to find it in docker secrets", sys.stderr)
    try:    
        return open('/run/secrets/' + key).read().strip()
    except FileNotFoundError:
        print("Key " + key + " not found in docker secrets", file=sys.stderr)
    return "KEY_NOT_FOUND"

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, True)
)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
CORE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Take environment variables from .env file
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY', default='S#perS3crEt_007')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

# Assets Management
ASSETS_ROOT = os.getenv('ASSETS_ROOT', '/static/assets') 

# load production server from .env
ALLOWED_HOSTS        = ['localhost', 'salespeach', 'localhost:85', '192.168.49.2', '127.0.0.1', '34.159.127.226', '0.0.0.0', '10.0.0.18', 'www.salespeach.org', env('SERVER', default='127.0.0.1') ]
CSRF_TRUSTED_ORIGINS = ['http://localhost:85', 'http://127.0.0.1', 'https://www.salespeach.org']

# Application definition

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  
EMAIL_FROM = 'salespeachgmbh@gmail.com'
EMAIL_USE_TLS = True  
EMAIL_PORT = 587  
EMAIL_HOST_USER = 'salespeachgmbh@gmail.com'  
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")  

PASSWORD_RESET_TIMEOUT = 14400


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'djstripe',
    'apps.authentication',
    # 'payments',
    # 'apps.home',                                    # Enable the inner home (home)
    'speach',
    # 'allauth',                                      # OAuth new
    # 'allauth.account',                              # OAuth new
    # 'allauth.socialaccount',                        # OAuth new 
    # 'allauth.socialaccount.providers.github',       # OAuth new 
    # 'allauth.socialaccount.providers.twitter',      # OAuth new  
    "sslserver"    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'
LOGIN_REDIRECT_URL = "home"  # Route defined in home/urls.py
LOGOUT_REDIRECT_URL = "home"  # Route defined in home/urls.py
TEMPLATE_DIR = os.path.join(CORE_DIR, "apps/templates")  # ROOT dir for templates

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apps.context_processors.cfg_assets_root',
            ],
        },
    },
]

STRIPE_TEST_PUBLIC_KEY = search_in_environment_or_docker_secrets("STRIPE_TEST_PUBLIC_KEY")
STRIPE_TEST_SECRET_KEY = search_in_environment_or_docker_secrets("STRIPE_TEST_SECRET_KEY")
print("STRIPE_TEST_SECRET_KEY " + STRIPE_TEST_SECRET_KEY)
logging.info("STRIPE_TEST_SECRET_KEY " + STRIPE_TEST_SECRET_KEY)

openai.api_key = "deprecated"
STRIPE_LIVE_MODE = False
DJSTRIPE_WEBHOOK_SECRET = os.getenv('DJSTRIPE_WEBHOOK_SECRET','NO_SECRETS')  # We don't use this, but it must be set
DJSTRIPE_FOREIGN_KEY_TO_FIELD = "id"
if DEBUG:
    DJSTRIPE_WEBHOOK_VALIDATION = 'retrieve_event'

OPEN_API_SERVICE = os.environ.get('OPEN_API_SERVICE', 'http://localhost:5000/')


WSGI_APPLICATION = 'core.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

if os.environ.get('DB_ENGINE') and os.environ.get('DB_ENGINE') == "mysql":
    logging.info("Using MySQL database")
    DATABASES = { 
      'default': {
        'ENGINE'  : 'django.db.backends.mysql', 
        'NAME'    : os.getenv('DB_NAME'     , 'appseed_db'),
        'USER'    : os.getenv('DB_USERNAME' , 'appseed_db_usr'),
        'PASSWORD': os.getenv('DB_PASS'     , 'pass'),
        'HOST'    : os.getenv('DB_HOST'     , 'mysql-server'),
        'PORT'    : os.getenv('DB_PORT'     , 3306),
        }, 
    }
else:
    logging.info("Using SQLite database")
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'db.sqlite3',
        }
    }

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

#############################################################
# SRC: https://devcenter.heroku.com/articles/django-assets

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
STATIC_ROOT = os.path.join(CORE_DIR, 'staticfiles')
STATIC_URL = '/static/'

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
    os.path.join(CORE_DIR, 'apps/static'),
) 

#############################################################
# OAuth settings 

GITHUB_ID     = os.getenv('GITHUB_ID', None)
GITHUB_SECRET = os.getenv('GITHUB_SECRET', None)
GITHUB_AUTH   = GITHUB_SECRET is not None and GITHUB_ID is not None

AUTHENTICATION_BACKENDS = (
    "core.custom-auth-backend.CustomBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)

SITE_ID                    = 1 
ACCOUNT_EMAIL_VERIFICATION = 'none'

SOCIALACCOUNT_PROVIDERS = {}

if GITHUB_AUTH:
    SOCIALACCOUNT_PROVIDERS['github'] = {
        'APP': {
            'client_id': GITHUB_ID,
            'secret': GITHUB_SECRET,
            'key': ''
        }
    }


#Payments stuff
# This can be a string or callable, and should return a base host that
# will be used when receiving callbacks and notifications from payment
# providers.
#
# Keep in mind that if you use `localhost`, external servers won't be
# able to reach you for webhook notifications.
PAYMENT_HOST = 'localhost:8000'

# Callable to retrieve payment provider instance
#
# This is an advanced setting. It is required if defining provider
# credentials in the settings file is unsuitable. Implementations may choose
# to read provider credentials from the database or any other source that's
# suitable.
#
# Alternatively, you can provide a callable that takes two arguments:
# variant (string) and an optional payment (BasePayment).
# The callback has to return an instance of the desired payment provider.
#
# For inspiration, see the payments.core.payment_factory function, which
# retrieves the variant from the above dictionary.
# PAYMENT_VARIANT_FACTORY = "mypaymentapp.provider_factory"
PAYMENT_MODEL = 'home.Payment'

PAYMENT_VARIANTS = {
    'default': ('payments.dummy.DummyProvider', {})
}
