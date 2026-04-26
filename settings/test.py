"""
Configuración de Django para entorno de pruebas
"""
from settings.base import *

# Configuración de base de datos para tests
DATABASES['default']['OPTIONS']['Trusted_Connection'] = 'yes'
DATABASES['default']['TEST'] = {
    'NAME': 'ross_crafts_test_db',  # BD separada para tests
}

# Desactivar logging durante tests
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
}

# Desactivar middleware de auditoría en tests
MIDDLEWARE = [m for m in MIDDLEWARE if 'audit' not in m.lower()]

# Configuración de email para tests
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

# Desactivar Stripe en tests
STRIPE_PUBLIC_KEY = 'pk_test_fake'
STRIPE_SECRET_KEY = 'sk_test_fake'
STRIPE_WEBHOOK_SECRET = 'whsec_test_fake'

# Password hashers más rápidos para tests
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

# Debug en tests
DEBUG = True
