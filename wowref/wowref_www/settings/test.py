from .base import *

SECRET_KEY = 'FIZZBUZZ'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'sqlite.db'
    },
}

DATABASE_ROUTERS = []
