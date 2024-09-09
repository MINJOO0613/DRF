from django.urls import path
from . import views


app_name = "products"
urlpatterns = [
    path("", views.ProductListView.as_view(), name="product_list_view"), # 상품 목록 조회, 상품 등록
    path("<int:pk>/", views.ProductDetailView.as_view(), name="product_detail_view"), # 상품 상세 조회, 상품 수정 및 삭제
    path('<int:product_id>/like/', views.ProductLikeAPI.as_view(), name='product_like'), # 게시물 좋아요
]
