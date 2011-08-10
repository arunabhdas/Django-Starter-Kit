# Local dev server.
from settings import *


# Environment
# ===========
SITE_ID = 1
DEBUG = True
TEMPLATE_DEBUG = DEBUG


# Databases
# ==========
DATABASES = {
    'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': '______',
            'USER': 'root',
            'PASSWORD': 'root',
            'HOST': '',
            'PORT': '',
            'OPTIONS': {
                "init_command": "SET storage_engine=INNODB",
            }
        }
    }


# Emails
# =======
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
