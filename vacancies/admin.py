from django.contrib import admin

from vacancies.models import Vacancy, Skill

admin.site.register(Vacancy)
admin.site.register(Skill)