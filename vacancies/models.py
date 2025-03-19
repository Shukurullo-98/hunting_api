from django.core.validators import MinValueValidator
from django.db import models

from authentication.models import User


class Skill(models.Model):
    name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Skills'
        ordering = ['name']
        verbose_name = 'Skill'

    def __str__(self):
        return self.name


class Vacancy(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ("open", "Open"),
        ("closed", "Closed"),
    )
    slug = models.SlugField(unique=True, max_length=100)
    text = models.CharField(max_length=2000)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    skills = models.ManyToManyField(Skill)
    likes = models.IntegerField(default=0, )
    min_experience = models.IntegerField(null=True, validators=[MinValueValidator(0)])

    class Meta:
        ordering = ('-created',)
        verbose_name_plural = 'Vacancies'
        verbose_name = 'Vacancy'

    def __str__(self):
        return self.slug

    @property
    def username(self):
        return self.user.username if self.user else None
