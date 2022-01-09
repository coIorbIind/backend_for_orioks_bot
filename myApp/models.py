import json

from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    telegram_username = models.CharField(max_length=50, verbose_name="Телеграмм аккаунт", unique=True)
    cookies = models.BinaryField(verbose_name="Печеньки")
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    marks = models.CharField(max_length=500, verbose_name="Оценки", blank=True)

    def __str__(self):
        return self.telegram_username

    def get_json_marks(self):
        return json.loads(self.marks)
