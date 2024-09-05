from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    GENDERS = (
        ('M', '남성(male)'),
        ('F', '여성(female)'),
    )

    name = models.CharField(verbose_name='이름', max_length=30)
    nickname = models.CharField(verbose_name='닉네임', max_length=20)
    date_of_birth = models.DateField(verbose_name='생년월일')
    gender = models.CharField(
        verbose_name='성별', 
        max_length=1, 
        choices=GENDERS,
        null=True,
        blank=True,
        )
    description = models.TextField(verbose_name='자기소개', null=True, blank=True)