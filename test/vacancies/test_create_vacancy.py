import os
from datetime import date

import pytest

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hunting_api.settings")

import django
django.setup()

@pytest.mark.django_db
def test_create_vacancy(client, hr_token):
    expected_response = {
        'count': 1,
        'next': None,
        'previous': None,
        'results': [{
            'id': 1,
            'text': '123e',
            'slug': '123e',
            'status': 'draft',
            'created': date.today().strftime("%Y-%m-%d"),
            'min_experience': None,
            'skills': [],
            'updated_at': None,
            'user': None,
            'likes': 0
        }]
    }
    data = {
        'slug': '1234e',
        'text': '1322',
        'status': 'draft'
    }
    response = client.post(
        "vacancy/create/",
        data,
        content_type='application/json',
        HTTP_AUTHORIZATION = "Token " + hr_token
    )
    assert response.status_code == 201
    assert response.data == expected_response







