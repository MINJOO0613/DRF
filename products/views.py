from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Product
from .serializers import ProductSerializer

# permission (IsAuthenticated/ReadOnly)
class ReadOnly(BasePermission):
    #읽기 전용 권한으로 설정함.
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS
    

# 페이지네이션
class ProductPagination(PageNumberPagination):
    page_size = 10  # 페이지당 10개 항목 반환
    page_size_query_param = 'page_size'
    max_page_size = 100  # 최대 페이지 크기 제한


class ProductListView(APIView):
    permission_classes = [IsAuthenticated | ReadOnly]

    # - 상품 목록 조회
    # endpoint: `/api/products`
    # Method: `GET`
    # 조건: 로그인 상태 불필요.
    # 구현: 모든 상품 목록 페이지네이션으로 반환.
    def get(self, request):
        products = Product.objects.all().order_by('-created_at')

        # 페이지네이터 객체 생성
        paginator = ProductPagination()
        paginated_products = paginator.paginate_queryset(products, request)

        serializer = ProductSerializer(paginated_products, many=True)
        return paginator.get_paginated_response(serializer.data)


    # - 상품 등록
    # Endpoint: `/api/products`
    # Method: `POST`
    # 조건: 로그인 상태, 제목과 내용, 상품 이미지 입력 필요.
    # 구현: 새 게시글 생성 및 데이터베이스 저장.
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProductDetailView(APIView):
    permission_classes = [IsAuthenticated | ReadOnly]

    def get_object(self, pk):
        return get_object_or_404(Product, pk=pk)

    # 상품 상세 조회
    def get(self, request, pk):
        product = self.get_object(pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    # - 상품 수정
    # Endpoint: `/api/products/<int:productId>`
    # Method: `PUT`
    # 조건: 로그인 상태, 수정 권한 있는 사용자(게시글 작성자)만 가능.
    # 검증: 요청자가 게시글의 작성자와 일치하는지 확인.
    # 구현: 입력된 정보로 기존 상품 정보를 업데이트.
    def put(self, request, pk):
        product = self.get_object(pk)

        if product.author != request.user:
            return Response({"message": "수정 권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)

        serializer = ProductSerializer(
            product, data=request.data, partial=True
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        
        
    # - 상품 삭제
    # Endpoint: `/api/products/<int:productId>`
    # Method: `DELETE`
    # 조건: 로그인 상태, 삭제 권한 있는 사용자(게시글 작성자)만 가능.
    # 검증: 요청자가 게시글의 작성자와 일치하는지 확인.
    # 구현: 해당 상품을 데이터베이스에서 삭제.
    def delete(self, request, pk):
        product = self.get_object(pk)

        if product.author != request.user:
            return Response({"message": "삭제 권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)
        
        product.delete()
        data = {"success": f"{pk}번 상품이 삭제되었습니다."}
        return Response(data, status=status.HTTP_204_NO_CONTENT)



# 게시글 좋아요 기능
class ProductLikeAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, product_id):
        product = get_object_or_404(Product, pk=product_id)
        user = request.user

        if not user in product.like_products.all():
            product.like_products.add(user)
            return Response({"message": "좋아요가 추가되었습니다.", "like_count": product.like_count}, status=status.HTTP_200_OK)
        else:
            product.like_products.remove(user)
            return Response({"message": "좋아요가 취소되었습니다.", "like_count": product.like_count}, status=status.HTTP_200_OK)

