from .models import User # User 모델
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "nickname",
            "email",
            "date_of_birth",
            ]
        

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username",
            "nickname",
            "email",
            "date_of_birth",
            "gender",
            'description',
            ]