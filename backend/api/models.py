from django.contrib.auth.models import AbstractUser 
from django.db import models

class User(AbstractUser ):
    age = models.PositiveIntegerField(null=True, blank=True)
    education = models.CharField(max_length=100, null=True, blank=True)
    specialty = models.CharField(max_length=100, null=True, blank=True)
    residence = models.CharField(max_length=100, null=True, blank=True)
    height = models.PositiveIntegerField(null=True, blank=True)
    weight = models.PositiveIntegerField(null=True, blank=True)
    dominant_hand = models.CharField(max_length=10, null=True, blank=True)
    diseases = models.TextField(null=True, blank=True)
    smoking = models.BooleanField(default=False)
    alcohol = models.BooleanField(default=False)
    sport = models.BooleanField(default=False)
    insomnia = models.BooleanField(default=False)
    current_mood = models.CharField(max_length=100, null=True, blank=True)  
    gamer = models.BooleanField(default=False)
    
    # Метод для получения информации о пользователе
    def get_user_info(self):
        return {
            "username": self.username,
            "age": self.age,
            "education": self.education,
            "specialty": self.specialty,
            "residence": self.residence,
            "height": self.height,
            "weight": self.weight,
            "dominant_hand": self.dominant_hand,
            "diseases": self.diseases,
            "smoking": self.smoking,
            "alcohol": self.alcohol,
            "sport": self.sport,
            "insomnia": self.insomnia,
            "current_mood": self.current_mood,
            "gamer": self.gamer,
        }

    class Meta:
        swappable = 'AUTH_USER_MODEL'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._meta.get_field('groups').remote_field.related_name = 'custom_user_groups'
        self._meta.get_field('user_permissions').remote_field.related_name = 'custom_user_permissions'


class TestNSI(models.Model):
    test_id = models.AutoField(primary_key=True)
    test_name = models.CharField(max_length=255)
    tittle_all = models.TextField()
    tittle_correct = models.TextField()

    def __str__(self):
        return self.test_name


class TestResults(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='results')
    test = models.ForeignKey(TestNSI, on_delete=models.CASCADE, related_name='results')
    try_number = models.PositiveIntegerField()
    number_all_answers = models.PositiveIntegerField()
    number_correct_answers = models.PositiveIntegerField()
    complete_time = models.DateTimeField(auto_now_add=True)
    accuracy = models.FloatField()

    def __str__(self):
        return f"{self.user.username} - {self.test.test_name} (Попытка {self.try_number})"
    