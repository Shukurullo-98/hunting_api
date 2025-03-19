import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hunting_api.settings")

import django
django.setup()


import pytest


@pytest.fixture
@pytest.mark.django_db
def hr_token(client, django_user_model):
    username = 'admin11'
    password = '123qwe'
    django_user_model.objects.create_user(
        username=username,
        password=password,
        role='hr'
    )

    response = client.post(
        "/user/login/",
        {'username': username, "password": password},
        format='json'
    )
    assert response.status_code == 201
    assert 'token' in response.data
    return response.data['token']