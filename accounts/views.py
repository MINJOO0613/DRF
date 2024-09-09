from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.permissions import IsAuthenticated
from .models import User
from .validators import validate_signup, validate_password_change, validate_profile
from .serializers import UserSerializer, ProfileSerializer


class ReadOnly(BasePermission):
    #읽기 전용 권한으로 설정함.
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class SignupView(APIView):
# 회원가입
# - Endpoint: `/api/accounts`
# - Method: `POST`
# - 조건: username, 비밀번호, 이메일, 이름, 닉네임, 생일 필수 입력하며 성별, 자기소개 생략 가능
# - 검증: username과 이메일은 유일해야 하며, 이메일 중복 검증(선택 기능).
# - 구현: 데이터 검증 후 저장.
    def post(self, request):
        # validation
        is_valid, err_msg = validate_signup(request.data)
        if not is_valid:
            return Response({"error":err_msg}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(
            username = request.data.get("username"),
            password = request.data.get("password"),
            first_name = request.data.get("first_name"),
            last_name = request.data.get("last_name"),
            email = request.data.get("email"),
            nickname = request.data.get("nickname"),
            date_of_birth = request.data.get("date_of_birth"),
        )

        serializer = UserSerializer(user)
        res_data = serializer.data
        refresh = RefreshToken.for_user(user)
        res_data["tokens"] = {
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh)
        }
        return Response(res_data, status=status.HTTP_201_CREATED)


# - 회원 탈퇴
# Endpoint: `/api/accounts`
# Method: `DELETE`
# 조건: 로그인 상태, 비밀번호 재입력 필요.
# 검증: 입력된 비밀번호가 기존 비밀번호와 일치해야 함.
# 구현: 비밀번호 확인 후 계정 삭제.
    def delete(self, request):
        user = request.user

        password = request.data.get("password")
        if not password or not check_password(password, user.password):
            return Response({"error": "비밀번호가 일치하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        # 회원탈퇴(계정 비활성화)
        user.soft_delete()
        return Response({"success": "계정이 성공적으로 탈퇴되었습니다."}, status=status.HTTP_204_NO_CONTENT)


# 로그인
# - Endpoint: `/api/accounts/login`
# - Method: `POST`
# - 조건: 사용자명과 비밀번호 입력 필요.
# - 검증: 사용자명과 비밀번호가 데이터베이스의 기록과 일치해야 함.
# - 구현: 성공적인 로그인 시 토큰을 발급하고, 실패 시 적절한 에러 메시지를 반환.
class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)

        # validation
        if not User.objects.filter(username=username).exists():
            return Response(
                {"error": "존재하지 않는 아이디입니다."}, status=status.HTTP_400_BAD_REQUEST
            )
        
        if not user:
            return Response(
                {"error": "패스워드가 틀렸습니다."}, status=status.HTTP_400_BAD_REQUEST
            )

        serializer = UserSerializer(user)
        res_data = serializer.data

        # token 발행
        refresh = RefreshToken.for_user(user)
        res_data["tokens"] = {
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh)
        }
        return Response(res_data)


# 로그아웃
# - Endpoint: `/api/accounts/logout`
# - Method: `POST`
# - 조건: 로그인 상태 필요.
# - 구현: 토큰 무효화 또는 다른 방법으로 로그아웃 처리 가능.
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token_str = request.data.get("refresh_token")
        try:
            refresh_token = RefreshToken(refresh_token_str)
        except TokenError:
            return Response(
                {"message": "해당 토큰은 사용할 수 없습니다."}, status=status.HTTP_400_BAD_REQUEST
            )

        refresh_token.blacklist()
        return Response({"success": "로그아웃 되었습니다."},status=status.HTTP_200_OK)


# 패스워드 변경
# - Endpoint: `/api/accounts/password`
# - Method: `PUT`
# - 조건: 기존 패스워드와 변경할 패스워드는 상이해야 함
# - 검증: 패스워드 규칙 검증
# - 구현: 패스워드 검증 후 데이터베이스에 업데이트.
class PasswordChangeView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        new_password = request.data.get("new_password")

        # validation
        is_valid, err_msg = validate_password_change(user, request.data)
        if not is_valid:
            return Response({"error":err_msg}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user.set_password(new_password)
            user.save()
            return Response({"msg":"비밀번호가 성공적으로 변경되었습니다."}, status=status.HTTP_201_CREATED)
        
        except ValidationError as e:
            return Response({"msg": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

class ProfileView(APIView):
    permission_classes = [IsAuthenticated | ReadOnly]

# 프로필 조회
# - Endpoint: `/api/accounts/<str:username>`
# - Method: `GET'
# - 조건: 로그인 상태 필요.
# - 검증: 로그인한 사용자만 프로필 조회 가능
# - 구현: 로그인한 사용자의 정보를 JSON 형태로 반환.
    def get(self, request, username):
        # 프로필 조회할 username 검색
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"error": "사용자를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProfileSerializer(user)
        return Response(serializer.data)
    
    # 프로필 수정(회원정보 수정)
    def put(self, request, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"error": "사용자를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)

        # 본인 프로필만 수정할 수 있음
        if user != request.user:
            return Response({"message": "수정 권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)
        
        # validation
        is_valid, err_msg = validate_profile(request.data)
        if not is_valid:
            return Response({"error":err_msg}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = ProfileSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)


# 팔로잉 시스템
# - 사용자 간의 ManyToMany 관계를 통한 팔로잉 기능
class FollowAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, username):
        user_to_follow = get_object_or_404(User, username=username)
        current_user = request.user

        if user_to_follow == current_user:
            return Response({"error": "본인의 계정을 팔로우할 수 없습니다."}, status=status.HTTP_400_BAD_REQUEST)

        if current_user.following.filter(username=username).exists():
            current_user.following.remove(user_to_follow)
            return Response({"message": "언팔로우되었습니다."}, status=status.HTTP_200_OK)
        else:
            current_user.following.add(user_to_follow)
            return Response({"message": "팔로우되었습니다."}, status=status.HTTP_200_OK)

