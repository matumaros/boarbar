import os

import django.conf.locale

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    'www.boar.bar',
    'www.custidioma.org',
    'www.servare.org',
]

SECRET_KEY = 'CHANGE THIS!!!'
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

INSTALLED_APPS = [
    # django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # third party
    'crispy_forms',
    'simple_history',
    'rest_framework',
    'rest_framework.authtoken',
    # project
    'share.apps.AppConfig',
    'dictionary.apps.DictionaryConfig',
    'user.apps.UserConfig',
    'collection.apps.CollectionConfig',
    'home.apps.HomeConfig',
    'word.apps.WordConfig',
    'sentence.apps.SentenceConfig',
    'language.apps.LanguageConfig',
    'proposal.apps.ProposalConfig',
    'course.apps.CourseConfig',
    'translator.apps.TranslatorConfig',
    'api.apps.ApiConfig',
]

MIDDLEWARE = [
    # django
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # third party
    'simple_history.middleware.HistoryRequestMiddleware',
]

ROOT_URLCONF = 'boar_bar.urls'

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

WSGI_APPLICATION = 'boar_bar.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'database',
        'USER': '',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}


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

gettext_noop = lambda s: s

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

LANGUAGES = (
    ('bv_DA', gettext_noop('Danube Bavarian')),
    ('bv_AL', gettext_noop('Alpine Bavarian')),
    ('bv_PL', gettext_noop('Palatinate Bavarian')),
)

EXTRA_LANG_INFO = {
    'bv_DA': {
        'bidi': False,  # right-to-left
        'code': 'bv_DA',
        'name': 'Danube Bavarian',
        'name_local': 'Donau Boariš',
    },
    'bv_AL': {
        'bidi': False,  # right-to-left
        'code': 'bv_AL',
        'name': 'Alpine Bavarian',
        'name_local': 'Óipm Boariš',
    },
    'bv_PL': {
        'bidi': False,  # right-to-left
        'code': 'bv_PL',
        'name': 'Palatinate Bavarian',
        'name_local': 'Pfóits Boariš',
    }
}

LANG_INFO = dict(
    list(django.conf.locale.LANG_INFO.items()) + list(EXTRA_LANG_INFO.items())
)
django.conf.locale.LANG_INFO = LANG_INFO

LANGUAGE_CODE = 'en'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS':
        'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    )
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'share', 'static')
STATICFILES_DIRS = []

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'share', 'media')

CRISPY_TEMPLATE_PACK = 'bootstrap3'

ADMINS = (('Mat', 'mat@boar.bar'),)
EMAIL_HOST = 'smtp.zoho.com'
EMAIL_HOST_USER = 'server@boar.bar'
EMAIL_HOST_PASSWORD = '<password>'
SERVER_EMAIL = 'server@boar.bar'

