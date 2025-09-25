"""
WSGI config for Hospital project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""
import sys
import os

# Add your project folder to sys.path
path = '/home/jayabalaji2k/Digital-Bank'
if path not in sys.path:
    sys.path.append(path)

# Set correct settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'Bank.settings'  # Use your project folder name

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
