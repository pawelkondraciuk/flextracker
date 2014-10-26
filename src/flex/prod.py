from settings import *

# DEBUG = False
#
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'd581qbk3rsti43',
#         'USER': 'bospdyakqoopnj',
#         'PASSWORD': 'zwuz3owT4cImHUZ3Uyi0gC73zD',
#         'HOST': 'ec2-54-246-88-248.eu-west-1.compute.amazonaws.com',
#         'PORT': '5432',
#     }
# }

# Parse database configuration from $DATABASE_URL
import dj_database_url
DATABASES['default'] = dj_database_url.config()

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

# Static asset configuration
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)