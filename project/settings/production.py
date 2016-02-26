# -*- encoding: utf-8 -*-

from project.settings.base import *

ALLOWED_HOSTS = get_secret('allowed_hosts')
SECRET_KEY = get_secret('secret_key')
DEBUG = False

STATIC_ROOT = get_secret('static_root')
MEDIA_ROOT = get_secret('media_root')

# EMAIL
SERVER_EMAIL = get_secret('server_email')
EMAIL_HOST = get_secret('email_host')
EMAIL_HOST_USER = get_secret('email_host_user')
EMAIL_HOST_PASSWORD = get_secret('email_host_password')
EMAIL_PORT = get_secret('email_port')
EMAIL_USE_SSL = get_secret('email_use_ssl')

ADMINS = tuple([(username, email)
                for username, email in get_secret('admins').items()])
TGM_SSL_SERT = get_secret('tgm_ssl_sert')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format':
            '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': get_secret('error_log'),
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'tgmbot': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': False,
        },
        'testapp': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': False,
        },
    },
}
