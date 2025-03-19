from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    MALE = 'm'
    FEMALE = 'f'
    SEX = [(MALE, "Male"), (FEMALE, 'Female')]

    HR = 'hr'
    EMPLOYEE = 'employee'
    UNKNOWN = 'unknown'

    ROLE = [(HR, HR), (EMPLOYEE, EMPLOYEE), (UNKNOWN, UNKNOWN)]

    sex = models.CharField(max_length=1, choices=SEX, default=MALE)
    role = models.CharField(choices=ROLE, max_length=8, default=UNKNOWN)
