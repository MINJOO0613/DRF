from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    # 좋아요 수 필드 추가
    like_count = serializers.IntegerField(read_only=True)

    # author를 사용자 이름으로 변환
    author = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'author', 'title', 'content', 'created_at', 'image', 'like_count']
        read_only_fields = ['id', 'author', 'created_at', 'updated_at','like_products']
        
    # author필드를 pk값이 아닌 usernamed으로 반환
    def get_author(self, obj):
        return obj.author.username