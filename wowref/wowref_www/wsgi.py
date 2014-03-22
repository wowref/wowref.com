"""
WSGI config for ophelia project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wowref_www.settings.production")

from wotlk.dbc import load_dbc_data
load_dbc_data()

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
