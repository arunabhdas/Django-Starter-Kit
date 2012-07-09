# Base settings
import os, sys

PROJECT_ROOT                        = os.path.dirname(__file__)

# Environment
# ===========
SITE_ID                             = 1
DEBUG                               = False
TEMPLATE_DEBUG                      = DEBUG

# Paths
# ======
sys.path.insert(0, os.path.join(PROJECT_ROOT, "lib"))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "apps"))

# static media
STATIC_ROOT                         = os.path.join(PROJECT_ROOT, 'static')
STATIC_URL                          = '/static/'
STATICFILES_DIRS                    = ()
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #'django.contrib.staticfiles.finders.DefaultStorageFinder',
    'compressor.finders.CompressorFinder',
)

# user uploaded files
MEDIA_ROOT                          = os.path.join(PROJECT_ROOT, 'media')
MEDIA_URL                           = '/media/'
ADMIN_MEDIA_PREFIX                  = '/static/admin/'


# Other django settings
# =====================
INTERNAL_IPS                        = ('127.0.0.1',)
LANGUAGE_CODE                       = 'en-us'
SECRET_KEY                          = ''
TIME_ZONE                           = 'UTC'
USE_TZ                              = True
USE_ETAGS                           = False
USE_I18N                            = False
USE_L10N                            = False
PREPEND_WWW                         = False
ROOT_URLCONF                        = 'urls'
#WSGI_APPLICATION                   = 'wsgi.application'

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

# Email settings
# ===============
ADMINS = (
    #('dev', 'dev@example.com'),
)
MANAGERS = ADMINS

EMAIL_BACKEND                       = 'django.core.mail.backends.console.EmailBackend'
SERVER_EMAIL                        = 'noreply@example.com'
EMAIL_HOST                          = ''
EMAIL_HOST_USER                     = ''
EMAIL_HOST_PASSWORD                 = ''
DEFAULT_FROM_EMAIL                  = SERVER_EMAIL
SEND_BROKEN_LINK_EMAILS             = False

# Apps & Middlewares
# ==================
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.flatpages',

    'analytical',
    'annoying',
    'compressor',
    'django_extensions',
    'gunicorn',
    'registration',
    'social_auth',
    'south',
    'pagination',

    'accounts',
    'main',
)

MIDDLEWARE_CLASSES = (
    #'django.middleware.common.GZipMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',

    'main.middlewares.AdminSecretMiddleware',
    'main.middlewares.ExceptionUserInfoMiddleware',
)

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
)

# Template settings
# ===============
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, 'templates'),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    "django.core.context_processors.request",
    'django.core.context_processors.static',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
)

# Logging
# =========
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}


# Sessions
# ========
SESSION_ENGINE                      = 'django.contrib.sessions.backends.cached_db'
SESSION_EXPIRE_AT_BROWSER_CLOSE     = False


# django-analytical
# ==================
CLICKY_SITE_ID                      = ''
CRAZY_EGG_ACCOUNT_NUMBER            = ''
GOOGLE_ANALYTICS_PROPERTY_ID        = ''


# django-registration
# =====================
LOGIN_REDIRECT_URL                  = '/'
LOGIN_URL                           = '/accounts/login/'
LOGOUT_URL                          = '/accounts/logout/'
AUTH_PROFILE_MODULE                 = 'accounts.UserProfile'

#--------------------
# django-social-auth
#--------------------
SOCIAL_AUTH_ERROR_KEY               = 'social_errors'
#SOCIAL_AUTH_PIPELINE                = ()


# Misc.
# ===================
ADMIN_SECRET                        = 'cloudshuffle'
DATABASE_BACKUP_ROOT                = '~/backups/'

try:
    from local_settings import *
except ImportError:
    pass
