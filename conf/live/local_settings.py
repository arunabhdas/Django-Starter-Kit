from settings import *


# Environment
# ===========
# Admin user: root
# Admin pass: _____________
SITE_ID = 3
DEBUG = False
TEMPLATE_DEBUG = DEBUG


# Databases
# ==========
DATABASES = {
    'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': '_______',
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
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
