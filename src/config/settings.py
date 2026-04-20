from decouple import config as decouple_config

# DATABASES - заменить полностью:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': decouple_config('DB_NAME'),
        'USER': decouple_config('DB_USER'),
        'PASSWORD': decouple_config('DB_PASSWORD'),
        'HOST': 'db',
        'PORT': '5432',
    }
}

# INSTALLED_APPS - добавить:
INSTALLED_APPS = [
    # ... стандартные
    'rest_framework',
]

# ALLOWED_HOSTS - заменить:
ALLOWED_HOSTS = decouple_config('ALLOWED_HOSTS', cast=lambda v: [s.strip() for s in v.split(',')])