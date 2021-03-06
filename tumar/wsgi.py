"""
WSGI config for viral project.
It exposes the WSGI callable as a module-level variable named ``application``.
For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/gunicorn/
"""
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tumar.config")
os.environ.setdefault("DJANGO_CONFIGURATION", "Production")

from configurations.wsgi import get_wsgi_application  # noqa

application = get_wsgi_application()
