from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.permissions import IsAuthenticated
from .models import User
from .validators import validate_signup
from .serializers import UserSerializer

# # 회원가입
# - Endpoint: `/api/accounts`
# - Method: `POST`
# - 조건: username, 비밀번호, 이메일, 이름, 닉네임, 생일 필수 입력하며 성별, 자기소개 생략 가능
# - 검증: username과 이메일은 유일해야 하며, 이메일 중복 검증(선택 기능).
# - 구현: 데이터 검증 후 저장.
class SignupView(APIView):
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
class LogoutView(APIView):
    def post(self, request):
        refresh_token_str = request.data.get("refresh_token")
        try:
            refresh_token = RefreshToken(refresh_token_str)
        except TokenError:
            return Response(
                {"message": "해당 토큰은 사용할 수 없습니다."}, status=status.HTTP_400_BAD_REQUEST
            )

        refresh_token.blacklist()
        return Response(status=status.HTTP_200_OK)


# 비밀번호 변경
class PasswordView(APIView):
    def put(self, request, username):
        user = get_object_or_404(User, username=username)

        password = user.password
        old_password = request.data.get("old_password")

        # validation
        if not check_password(old_password, password):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        new_password = request.data.get("new_password")
        new_password2 = request.data.get("new_password2")

        if new_password != new_password2 :
            return Response({"msg":"비밀번호가 일치하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        # 비밀번호 해싱처리 및 변경된 비밀번호로 저장
        try:
            user.set_password(new_password)
            user.save()
            return Response({"msg":"비밀번호가 성공적으로 변경되었습니다."}, status=status.HTTP_201_CREATED)
        
        except ValidationError as e:
            return Response({"msg": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

# #프로필 조회
# - Endpoint: `/api/accounts/<str:username>`
# - Method: `GET'
# - 조건: 로그인 상태 필요.
# - 검증: 로그인한 사용자만 프로필 조회 가능
# - 구현: 로그인한 사용자의 정보를 JSON 형태로 반환.
class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    # 프로필 조회
    def get(self, request, username):
        user = User.objects.get(username=username)
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
    # 회원정보 수정
    def put(self, reqeust, username):
        pass



