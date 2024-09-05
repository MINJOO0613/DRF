from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .validators import validate_signup
from .serializers import UserSerializer

#회원가입
class SignupView(APIView):
    def post(self, request):
        # valitdation
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

        return Response(serializer.data, status=status.HTTP_201_CREATED)


#로그인
class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)

        if not User.objects.filter(username=username).exists():
            return Response(
                {"error": "존재하지 않는 아이디입니다."}, status=status.HTTP_400_BAD_REQUEST
            )
        
        if not user:
            return Response(
                {"error": "패스워드가 틀렸습니다."}, status=status.HTTP_400_BAD_REQUEST
            )

        serializer = UserSerializer(user)
        return Response(serializer.data)