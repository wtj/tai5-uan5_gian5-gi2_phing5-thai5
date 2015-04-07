"""
Django settings for tai5uan5_gian5gi2_phing5thai5 project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '$26ktnn8evagv3z31i5btlne4lj8-)=by6j^ed3k#z6gx04yrk'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['localhost']


# Application definition

INSTALLED_APPS = (
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
# 	allauth
	# The Django sites framework is required for allauth
	'django.contrib.sites',
	'allauth',
	'allauth.account',
	'allauth.socialaccount',
	'allauth.socialaccount.providers.facebook',
	'allauth.socialaccount.providers.google',
# 	家己的
	'臺灣言語資料庫',
	'臺灣言語平臺',
)

MIDDLEWARE_CLASSES = (
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'tai5uan5_gian5gi2_phing5thai5.urls'

WSGI_APPLICATION = 'tai5uan5_gian5gi2_phing5thai5.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.sqlite3',
		'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
	}
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

TEMPLATE_CONTEXT_PROCESSORS = (
	# Required by allauth template tags
	"django.core.context_processors.request",
	# allauth specific context processors
	"allauth.account.context_processors.account",
	"allauth.socialaccount.context_processors.socialaccount",
	'django.contrib.auth.context_processors.auth',
)
AUTHENTICATION_BACKENDS = (
	# Needed to login by username in Django admin, regardless of `allauth`
	"django.contrib.auth.backends.ModelBackend",
	# `allauth` specific authentication methods, such as login by e-mail
	"allauth.account.auth_backends.AuthenticationBackend",
)

SOCIALACCOUNT_PROVIDERS = \
	{'facebook':
		{'SCOPE': ['email',],
		'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
		'METHOD': 'js_sdk',
		'LOCALE_FUNC': lambda request: 'zh_TW',
		'VERIFIED_EMAIL': False,
		'VERSION': 'v2.3',
		}
	}
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_UNIQUE_EMAIL = True

ACCOUNT_ADAPTER='臺灣言語平臺.使用者模型.使用者接口'
SOCIALACCOUNT_ADAPTER ='臺灣言語平臺.使用者模型.社接口'

SITE_ID = 1
AUTH_USER_MODEL = '臺灣言語平臺.使用者表'

# 使用者上傳檔案
MEDIA_ROOT = os.path.join(BASE_DIR, "資料庫影音檔案")
MEDIA_URL = '/影音檔案/'
