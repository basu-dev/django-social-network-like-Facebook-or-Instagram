
import os
import django_heroku
import whitenoise
from .secret import My_SECRET
import cloudinary
import cloudinary_storage
import cloudinary.uploader
import cloudinary.api
# import gdstorage
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = My_SECRET

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["sbraven.herokuapp.com"]
ALLOWED_HOSTS = ["*"]

ROOT_URLCONF = 'SocialNetwork.urls'

# Application definition

INSTALLED_APPS = [
    "message",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "whitenoise.runserver_nostatic",
    "django.contrib.staticfiles",
    "stories",
    "Friends",
    'cloudinary_storage',
    'cloudinary',
    'pwa'
    # 'gdstorage'
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]



TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "stories.own_context_preprocessor.cloudinary_url"
            ]
        },
    }
]

WSGI_APPLICATION = "SocialNetwork.wsgi.application"

CLOUDINARY_URL='https://res.cloudinary.com/sbraven/image/upload/v1/'
# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = "/static/"
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
# MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/storage/"
# MEDIA_ROOT = 'cloudinary_storage.storage.MediaCloudinaryStorage'
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'



django_heroku.settings(locals())
cloudinary.config( 
  cloud_name = "sbraven", 
  api_key = "389368883326524", 
  api_secret = "-hUkaLSbLj6nmd5-tmPDGtaP45U" 
)
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': 'sbraven',
    'API_KEY': '389368883326524',
    'API_SECRET': '-hUkaLSbLj6nmd5-tmPDGtaP45U'
}
# for pwa
PWA_SERVICE_WORKER_PATH = os.path.join(BASE_DIR, 'serviceworker.js')

PWA_APP_NAME = 'Raven'
PWA_APP_DESCRIPTION = "Raven"
PWA_APP_THEME_COLOR = '#013244'
PWA_APP_BACKGROUND_COLOR = '#086384'
PWA_APP_DISPLAY = 'standalone'
PWA_APP_SCOPE = '/'
PWA_APP_ORIENTATION = 'any'
PWA_APP_START_URL = '/'
PWA_APP_STATUS_BAR_COLOR = 'default'
PWA_APP_ICONS = [
	{
		'src':'https://res.cloudinary.com/sbraven/image/upload/v1606766517/static/144_fhnyii.png',
		'sizes': '144x144'
	}
]
PWA_APP_ICONS_APPLE = [
	{
		'src': 'https://res.cloudinary.com/sbraven/image/upload/v1606766517/static/144_fhnyii.png',
		'sizes': '144x144'
	},
    {
        'src': 'https://res.cloudinary.com/sbraven/image/upload/v1606766518/static/512_p0mdw2.png',
        'sizes': '512x512'
    }
]
PWA_APP_SPLASH_SCREEN = [
	{
		'src': 'https://res.cloudinary.com/sbraven/image/upload/v1606766518/static/512_p0mdw2.png',
		'media': '(device-width: 320px) and (device-height: 568px) and (-webkit-device-pixel-ratio: 2)'
	}
]
PWA_APP_DIR = 'ltr'
PWA_APP_LANG = 'en-US'

