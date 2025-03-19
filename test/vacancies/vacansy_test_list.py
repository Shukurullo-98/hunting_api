import os
from datetime import date

import pytest

from vacancies.models import Vacancy

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hunting_api.settings")

import django
django.setup()

@pytest.mark.django_db
def test_vacancy_list(client):
    vacancy = Vacancy.objects.create(
        slug='123e',
        text='123e'
    )
    expected_response = {
        'count': 1,
        'next': None,
        'previous': None,
        'results': [{
            'id': vacancy.pk,
            'text': '123e',
            'slug': '123e',
            'status': 'draft',
            'created': date.today().strftime("%Y-%m-%d"),
            'username': None,
            'skills': []
        }]
    }
    response = client.get("vacancy/")
    assert response.status_code == 200
    assert response.data == expected_response
