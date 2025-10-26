"""
WSGI config for dron_site project.
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dron_site.settings')

application = get_wsgi_application()
