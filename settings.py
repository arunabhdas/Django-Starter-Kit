# Base settings
import os, sys

PROJECT_ROOT                        = os.path.dirname(__file__)

# Environment
# ===========
SITE_ID                             = 1
DEBUG                               = True
TEMPLATE_DEBUG                      = DEBUG

# Paths
# ======
sys.path.insert(0, os.path.join(PROJECT_ROOT, "lib"))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "apps"))
MEDIA_URL                           = '/media/'
ADMIN_MEDIA_PREFIX                  = '/media/admin/'
MEDIA_ROOT                          = os.path.join(PROJECT_ROOT, 'media')

# Other django settings
# =====================
INTERNAL_IPS                        = ('127.0.0.1',)
LANGUAGE_CODE                       = 'en-us'
SECRET_KEY                          = '4n7tg$vmh^y4p7z4tahfa8x#r!_j7g580m*=mh&dj!-jyo6f%x' # Todo: Change this
TIME_ZONE                           = 'Etc/UTC'
USE_ETAGS                           = True
USE_I18N                            = False
USE_L10N                            = False
PREPEND_WWW                         = True
ROOT_URLCONF                        = 'urls'
ADMIN_SECRET                        = 'cloudshuffle'
DATABASE_BACKUP_ROOT                = '~/backups/'

# Databases
# ==========
# over ride in local_settings
DATABASES                           = {}

# Email settings
# ===============
ADMINS = (
    #('dev', 'dev@example.com'),
)
MANAGERS = ADMINS

# Apps & Middlewares
# ==================
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.flatpages',

    'analytical',
    'compressor',
    'django_extensions',
    'gunicorn',
    'south',
)

MIDDLEWARE_CLASSES = (
    #'django.middleware.common.GZipMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
    'common.middlewares.SetCookieForProtectedEnvironment',
    'common.middlewares.ExceptionUserInfoMiddleware',
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
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    "django.contrib.messages.context_processors.messages",
)

# Email
# ======
EMAIL_BACKEND                       = 'django.core.mail.backends.console.EmailBackend'
#EMAIL_BACKEND                      = 'django.core.mail.backends.smtp.EmailBackend'
SERVER_EMAIL                        = 'noreply@example.com'
EMAIL_HOST                          = ''
EMAIL_HOST_USER                     = ''
EMAIL_HOST_PASSWORD                 = ''
DEFAULT_FROM_EMAIL                  = SERVER_EMAIL
SEND_BROKEN_LINK_EMAILS             = False

# Sessions
# ========
SESSION_ENGINE                      = 'django.contrib.sessions.backends.cached_db'
SESSION_EXPIRE_AT_BROWSER_CLOSE     = False

# Registration
# ============
#AUTH_PROFILE_MODULE                 = 'accounts.UserProfile'
#LOGIN_REDIRECT_URL                  = '/'

try:
    from local_settings import *
except ImportError:
    pass
