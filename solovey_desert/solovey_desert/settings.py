import environ
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(
    DEBUG=(bool, False),
    ALLOWED_HOSTS=(list, ['localhost', '127.0.0.1']),
    CSRF_TRUSTED_ORIGINS=(list, []),
)
environ.Env.read_env(BASE_DIR.parent / '.env')
environ.Env.read_env(BASE_DIR / '.env')


SECRET_KEY = env('SECRET_KEY', default='django-insecure-local-dev-key-change-me')
DEBUG = env('DEBUG')
ALLOWED_HOSTS = env('ALLOWED_HOSTS')
CSRF_TRUSTED_ORIGINS = env('CSRF_TRUSTED_ORIGINS')

INSTALLED_APPS = [
    'unfold',
    'unfold.contrib.filters',
    'unfold.contrib.forms',
    'unfold.contrib.inlines',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sitemaps',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'django_filters',

    'apps.catalog',
    'apps.pages',
    'apps.orders',
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

ROOT_URLCONF = 'solovey_desert.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apps.pages.context_processors.site_settings',
            ],
        },
    },
]

WSGI_APPLICATION = 'solovey_desert.wsgi.application'
ASGI_APPLICATION = 'solovey_desert.asgi.application'

if env('POSTGRES_DB', default=''):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': env('POSTGRES_DB'),
            'USER': env('POSTGRES_USER', default='postgres'),
            'PASSWORD': env('POSTGRES_PASSWORD', default=''),
            'HOST': env('POSTGRES_HOST', default='localhost'),
            'PORT': env.int('POSTGRES_PORT', default=5432),
            'CONN_MAX_AGE': env.int('POSTGRES_CONN_MAX_AGE', default=60),
            'OPTIONS': {
                'connect_timeout': env.int('POSTGRES_CONNECT_TIMEOUT', default=5),
            },
        }
    }
else:
    DATABASES = {
        'default': env.db('DATABASE_URL', default=f'sqlite:///{BASE_DIR / "db.sqlite3"}')
    }

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


LANGUAGE_CODE = 'ru'

TIME_ZONE = env('TIME_ZONE', default='Europe/Minsk')

USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
}

SESSION_COOKIE_AGE = 60 * 60 * 24 * 30
SESSION_COOKIE_SECURE = env.bool('SESSION_COOKIE_SECURE', default=not DEBUG)
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
CSRF_COOKIE_SECURE = env.bool('CSRF_COOKIE_SECURE', default=not DEBUG)

CART_COOKIE_NAME = 'solovey_cart_id'
CART_COOKIE_AGE = env.int('CART_COOKIE_AGE', default=60 * 60 * 24 * 180)
CART_COOKIE_SECURE = env.bool('CART_COOKIE_SECURE', default=not DEBUG)
CART_MAX_ITEM_QUANTITY = env.int('CART_MAX_ITEM_QUANTITY', default=99)

SITE_URL = env('SITE_URL', default='http://127.0.0.1:8000').rstrip('/')
SITE_NAME = env('SITE_NAME', default='Solovey Desert')
SITE_DESCRIPTION = env(
    'SITE_DESCRIPTION',
    default='Авторские торты, десерты, конфеты и подарочные наборы ручной работы в Минске.',
)
SITE_PHONE = env('SITE_PHONE', default='+375 (29) 123-45-67')
SITE_EMAIL = env('SITE_EMAIL', default='solovey.desert@gmail.com')
SITE_CITY = env('SITE_CITY', default='Минск')
YANDEX_METRICA_ID = env('YANDEX_METRICA_ID', default='')
YANDEX_WEBMASTER_VERIFICATION = env('YANDEX_WEBMASTER_VERIFICATION', default='')
GOOGLE_SITE_VERIFICATION = env('GOOGLE_SITE_VERIFICATION', default='')
GOOGLE_ANALYTICS_ID = env('GOOGLE_ANALYTICS_ID', default='')

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_HSTS_SECONDS = env.int('SECURE_HSTS_SECONDS', default=0)
SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool('SECURE_HSTS_INCLUDE_SUBDOMAINS', default=False)
SECURE_HSTS_PRELOAD = env.bool('SECURE_HSTS_PRELOAD', default=False)

UNFOLD = {
    'SITE_TITLE': 'Solovey Desert admin',
    'SITE_HEADER': 'Solovey Desert',
    'SITE_SUBHEADER': 'Каталог, корзины и заявки',
    'SITE_SYMBOL': 'cake',
    'SHOW_HISTORY': True,
    'SHOW_VIEW_ON_SITE': True,
}


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
