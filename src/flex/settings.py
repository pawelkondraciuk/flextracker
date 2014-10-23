"""
Django settings for flex project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '7wl-2ubsqrpa^5xwh25tx8&sg_&(7wqcahooo3bfj2^&px_*4%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'grappelli',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.comments',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    ###########################
    'accounts',
    'dashboard',
    'projects',
    'issues',
    'attachments',
    'workflow',
    ###########################
    'south',
    'django_activeurl',
    'bootstrap3',
    'userena',
    'guardian',
    'accounts',
    'sitetree',
    #'viewflow',
    #'viewflow.site',
    'django_tables2',
    'taggit',
    'sorl.thumbnail',
    'django_messages',
    'widget_tweaks',
    'actstream',
    'genericadmin',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'userena.middleware.UserenaLocaleMiddleware',
    'django_tools.middlewares.ThreadLocal.ThreadLocalMiddleware'
)

AUTHENTICATION_BACKENDS = (
    'userena.backends.UserenaAuthenticationBackend',
    'guardian.backends.ObjectPermissionBackend',
    'django.contrib.auth.backends.ModelBackend',
)


TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',
    'projects.context_processors.project_list',
    'django_messages.context_processors.inbox',
)

ROOT_URLCONF = 'flex.urls'

WSGI_APPLICATION = 'flex.wsgi.application'

SITE_ID = 1

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

# DATABASES = {
# 'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'flex_tracker',
        'USER': 'postgres',
        'PASSWORD': 'password',
        'HOST': '192.168.56.101',
        'PORT': '5432',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'site_media', 'media')
MEDIA_URL = '/site_media/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': True,
#     'formatters': {
#         'standard': {
#             'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
#             'datefmt' : "%d/%b/%Y %H:%M:%S"
#         },
#     },
#     'handlers': {
#         'null': {
#             'level':'DEBUG',
#             'class':'django.utils.log.NullHandler',
#         },
#         'logfile': {
#             'level':'DEBUG',
#             'class':'logging.handlers.RotatingFileHandler',
#             'filename': "logfile.txt",
#             'maxBytes': 50000,
#             'backupCount': 2,
#             'formatter': 'standard',
#         },
#         'console':{
#             'level':'INFO',
#             'class':'logging.StreamHandler',
#             'formatter': 'standard'
#         },
#     },
#     # 'loggers': {
#     #     'django': {
#     #         'handlers': ['logfile'],
#     #         'propagate': True,
#     #         'level': 'ERROR',
#     #     },
#     # }
# }

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'fl3x.tracker@gmail.com'
EMAIL_HOST_PASSWORD = 'flextracke'

ANONYMOUS_USER_ID = -1
AUTH_PROFILE_MODULE = 'accounts.UserProfile'

LOGIN_URL = '/accounts/signin/'
LOGOUT_URL = '/accounts/signout/'

BOOTSTRAP3 = {
    'field_renderers': {
        'default': 'utils.bootstrap_render.CustomFieldRenderer',
        'inline': 'bootstrap3.renderers.InlineFieldRenderer',
    },
}