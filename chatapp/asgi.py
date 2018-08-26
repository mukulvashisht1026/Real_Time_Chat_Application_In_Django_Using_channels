import os
import django
from channels.routing import get_default_application

os.environ.setdefault("DJANGO_SETTING_MODULE","chatapp.settings")
django.setup()
application = get_default_application()

