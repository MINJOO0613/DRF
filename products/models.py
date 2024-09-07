from django.db import models
from django.conf import settings

class Product(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="products"
    )
    title = models.CharField(max_length=120)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to="images/", blank=True)


    def __str__(self):
        return self.title
    # likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="like_products")
    
    # 게시글 좋아요 기능
    # @property
    # def like_count(self):
    #     return self.likes.count()
