import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hunting_api.settings")

import django
django.setup()

def test_root_not_found(client):
    response = client.get('/')
    assert response.status_code == 404