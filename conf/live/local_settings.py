# Local dev server.
from settings import *


# Environment
# ===========
# Admin user: root
# Admin pass: _________
SITE_ID = 3
DEBUG = False
TEMPLATE_DEBUG = DEBUG


# Databases
# ==========
DATABASES = {
    'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': '',
            'USER': '',
            'PASSWORD': '',
            'HOST': '',
            'PORT': '',
            'OPTIONS': {
                "init_command": "SET storage_engine=INNODB",
            }
        }
    }

# Emails
# =======
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
