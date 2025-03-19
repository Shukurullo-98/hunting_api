from logging import makeLogRecord

from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=150)
    logo = models.ImageField(upload_to='logos/')