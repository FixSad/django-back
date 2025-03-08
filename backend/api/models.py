from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    age = models.PositiveIntegerField(null=True, blank=True)  # Возраст
    education = models.CharField(max_length=100, null=True, blank=True)  # Образование
    specialty = models.CharField(max_length=100, null=True, blank=True)  # Специальность
    residence = models.CharField(max_length=100, null=True, blank=True)  # Место жительства
    height = models.PositiveIntegerField(null=True, blank=True)  # Рост
    weight = models.PositiveIntegerField(null=True, blank=True)  # Вес
    dominant_hand = models.CharField(max_length=10, null=True, blank=True)  # Ведущая рука
    diseases = models.TextField(null=True, blank=True)  # Заболевания
    smoking = models.BooleanField(default=False)  # Курение
    alcohol = models.BooleanField(default=False)  # Алкоголь
    sport = models.BooleanField(default=False)  # Спорт
    insomnia = models.BooleanField(default=False)  # Бессонница
    current_mood = models.CharField(max_length=100, null=True, blank=True)  # Текущее самочувствие
    gamer = models.BooleanField(default=False)  # Геймер

    class Meta:
        # Указываем уникальные related_name для полей groups и user_permissions
        swappable = 'AUTH_USER_MODEL'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._meta.get_field('groups').remote_field.related_name = 'custom_user_groups'
        self._meta.get_field('user_permissions').remote_field.related_name = 'custom_user_permissions'