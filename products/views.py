from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Product
from .serializers import ProductSerializer


class ProductListView(APIView):
# - 상품 목록 조회
#     endpoint: `/api/products`
#     Method: `GET`
#     조건: 로그인 상태 불필요.
#     구현: 모든 상품 목록 페이지네이션으로 반환.
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# - 상품 등록
#     Endpoint: `/api/products`
#     Method: `POST`
#     조건: 로그인 상태, 제목과 내용, 상품 이미지 입력 필요.
#     구현: 새 게시글 생성 및 데이터베이스 저장.
    def post(self, request):
        # permission_classes = [IsAuthenticated]
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)



# - 상품 수정
#     Endpoint: `/api/products/<int:productId>`
#     Method: `PUT`
#     조건: 로그인 상태, 수정 권한 있는 사용자(게시글 작성자)만 가능.
#     검증: 요청자가 게시글의 작성자와 일치하는지 확인.
#     구현: 입력된 정보로 기존 상품 정보를 업데이트.
# - 상품 삭제
#     Endpoint: `/api/products/<int:productId>`
#     Method: `DELETE`
#     조건: 로그인 상태, 삭제 권한 있는 사용자(게시글 작성자)만 가능.
#     검증: 요청자가 게시글의 작성자와 일치하는지 확인.
#     구현: 해당 상품을 데이터베이스에서 삭제.