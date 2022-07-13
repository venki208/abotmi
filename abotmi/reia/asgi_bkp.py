import os
import django
from channels.routing import get_default_application
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "reia.[SETTINGS]")
django.setup()
application = get_default_application()
