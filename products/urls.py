from django.urls import path
from . import views


app_name = "products"
urlpatterns = [
    path("", views.ProductListView.as_view(), name="product_list_view"),
    path("<int:pk>/", views.ProductDetailView.as_view(), name="product_detail_view"),
    # path('<int:product_id>/like/', views.ProductLikeAPI.as_view(), name='product_like'), #좋아요
]
