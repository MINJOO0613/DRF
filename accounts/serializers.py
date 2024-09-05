from .models import User # User 모델
from rest_framework import serializers

class SignupSerializer(serializer.ModelSerializer):
    class Meta:
        model = User
        fields = ["pk", "username", "password", "email"]
    