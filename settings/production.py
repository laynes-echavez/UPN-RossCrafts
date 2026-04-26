"""
Configuración de Django para entorno de producción
"""
from .base import *
import os

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')

# SQL Server Express - Producción
# Usa autenticación de Windows (Trusted_Connection)
DATABASES = {
    'default': {
        'ENGINE': 'mssql',
        'NAME': env('DB_NAME'),
        'HOST': env('DB_HOST'),
        'PORT': '',
        'OPTIONS': {
            'driver': 'ODBC Driver 17 for SQL Server',
            'Trusted_Connection': 'yes',
            'TrustServerCertificate': 'no',  # Certificado válido en producción
        },
    }
}

# Archivos estáticos con WhiteNoise
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Asegurar que WhiteNoise esté en middleware
if 'whitenoise.middleware.WhiteNoiseMiddleware' not in MIDDLEWARE:
    MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

# Seguridad HTTPS
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000  # 1 año
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Seguridad adicional
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Email en producción
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL')

# Stripe modo live (producción)
STRIPE_PUBLIC_KEY = env('STRIPE_PUBLIC_KEY')  # pk_live_...
STRIPE_SECRET_KEY = env('STRIPE_SECRET_KEY')  # sk_live_...
STRIPE_WEBHOOK_SECRET = env('STRIPE_WEBHOOK_SECRET')

# Logging mejorado para producción
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'detailed': {
            'format': '{asctime} | {levelname} | {module} | {message}',
            'style': '{',
        },
    },
    'handlers': {
        'error_file': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR / 'logs/errors.log',
            'maxBytes': 10485760,  # 10MB
            'backupCount': 5,
            'formatter': 'detailed',
        },
        'warning_file': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR / 'logs/warnings.log',
            'maxBytes': 10485760,
            'backupCount': 5,
            'formatter': 'detailed',
        },
        'activity_file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR / 'logs/activity.log',
            'maxBytes': 10485760,
            'backupCount': 5,
            'formatter': 'detailed',
        },
    },
    'loggers': {
        'apps.sales': {
            'handlers': ['activity_file', 'error_file'],
            'level': 'INFO',
        },
        'apps.payments': {
            'handlers': ['activity_file', 'error_file'],
            'level': 'INFO',
        },
        'django': {
            'handlers': ['error_file', 'warning_file'],
            'level': 'WARNING',
        },
        'django.security': {
            'handlers': ['error_file'],
            'level': 'ERROR',
        },
    },
}

# Session settings para producción
SESSION_COOKIE_AGE = 1800  # 30 minutos
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'

# CSRF settings
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = 'Lax'
CSRF_USE_SESSIONS = False

# Admins para notificaciones de errores
ADMINS = [
    ('Admin Ross Crafts', env('ADMIN_EMAIL', default='admin@rosscrafts.com')),
]

MANAGERS = ADMINS

# Cache (opcional - usar si se necesita)
# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
#         'LOCATION': 'ross-crafts-cache',
#     }
# }
