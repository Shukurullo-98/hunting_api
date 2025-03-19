import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hunting_api.settings")

import django
django.setup()


pytest_plugin = 'test.fixture'