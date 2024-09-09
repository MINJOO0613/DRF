from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class User(AbstractUser):
    GENDERS = (
        ('M', '남성(male)'),
        ('F', '여성(female)'),
    )

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
    followers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='following', blank=True)
    

    # 회원탈퇴 시, 계정을 비활성화 상태로 변경
    def soft_delete(self):
        self.is_active = False
        self.save()


    @property
    def follower_count(self):
        return self.followers.count()

    @property
    def following_count(self):
        return self.following.count()