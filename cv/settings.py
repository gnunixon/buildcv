"""
Django settings for cv project.

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
SECRET_KEY = '3f!caeykx-3ecpw5*9a_ez5a3chbvz9i15c!3+)^0q#dw_u_-8'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'udata',
    'django_rq',
    'hvad',
    'social.apps.django_app.default',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'cv.urls'

WSGI_APPLICATION = 'cv.wsgi.application'

TEMPLATE_CONTEXT_PROCESSORS = (
       'django.contrib.auth.context_processors.auth',
       'django.core.context_processors.debug',
       'django.core.context_processors.i18n',
       'django.core.context_processors.media',
       'django.core.context_processors.static',
       'django.core.context_processors.tz',
       'django.contrib.messages.context_processors.messages',
       'social.apps.django_app.context_processors.backends',
       'social.apps.django_app.context_processors.login_redirect',
)

AUTHENTICATION_BACKENDS = (
       'social.backends.facebook.FacebookOAuth2',
       'django.contrib.auth.backends.ModelBackend',
)

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': '',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
        'TEST_CHARSET': "utf8",
        'TEST_COLLATION': "utf8_general_ci",
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'ro-ro'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOCALE_PATHS = (
        os.path.join(BASE_DIR, 'locale'),
)
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/
MEDIA_ROOT = os.path.join(BASE_DIR, 'img')
MEDIA_URL = '/img/'
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

RQ_QUEUES = {
    'default': {
                'HOST': '',
                'PORT': 6379,
                'DB': 0,
                'DEFAULT_TIMEOUT': 360,
            },
    'high': {
                'HOST': '',
                'PORT': 6379,
                'DB': 0,
                'DEFAULT_TIMEOUT': 360,
            }
}

LOGIN_REDIRECT_URL = '/'
SOCIAL_AUTH_FACEBOOK_KEY = ''
SOCIAL_AUTH_FACEBOOK_SECRET = ''
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email', 'user_work_history', 'user_education_history']

EMAIL_HOST = ''
EMAIL_PORT = 587
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = True
