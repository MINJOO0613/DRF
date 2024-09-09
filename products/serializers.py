from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'author', 'title', 'content', 'created_at', 'image']
        read_only_fields = ['id', 'author', 'created_at', 'updated_at','like_users']


# class ProductDetailSerializer(serializers.ModelSerializer):
#     class Meta:
