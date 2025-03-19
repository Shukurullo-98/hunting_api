from django.urls import path
from .views import *

urlpatterns = [
    path('<int:pk>/image/', CompanyImageView.as_view())
]