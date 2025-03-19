from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'skill', SkillsViewSet, basename='skill')


urlpatterns = [
    path('', VacancyView.as_view(), name='vacancy'),
    path('<int:pk>/', VacancyDetailView.as_view(), name='vacancy_detail_view'),
    path('create/', VacancyCreateView.as_view(), name='vacancy_create_view'),
    path('<int:pk>/update/', VacancyUpdateView.as_view(), name='vacancy_update_view'),
    path('<int:pk>/delete/', VacancyDeleteView.as_view(), name='vacancy_delete_view'),
    path('by-user/', user_vacancies ),
    path('like/', VacancyLikeView.as_view(), ),

]
urlpatterns += router.urls
