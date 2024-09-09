from .models import User
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
    follower_count = serializers.IntegerField(read_only=True)
    following_count = serializers.IntegerField(read_only=True)

    followers = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "username",
            "nickname",
            "email",
            "date_of_birth",
            "gender",
            'description',
            "follower_count",
            "followers",
            "following_count",
            ]
        read_only_fields = ["followers", "follower_count", "following_count"]

    # follwers필드를 pk값이 아닌 username으로 반환
    def get_followers(self, obj):
        return [follower.username for follower in obj.followers.all()]