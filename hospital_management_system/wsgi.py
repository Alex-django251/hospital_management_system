import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_management_system.settings')

# Vercel requires a top-level variable named "app"
application = get_wsgi_application()
app = application
