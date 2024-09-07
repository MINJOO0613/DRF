from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
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


# #프로필 조회
# - Endpoint: `/api/accounts/<str:username>`
# - Method: `GET'
# - 조건: 로그인 상태 필요.
# - 검증: 로그인한 사용자만 프로필 조회 가능
# - 구현: 로그인한 사용자의 정보를 JSON 형태로 반환.
class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, username):
        user = User.objects.get(username=username)
        serializer = UserSerializer(user)
        return Response(serializer.data)
