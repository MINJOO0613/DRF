from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User




class SignupView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        first_name = request.data.get("first_name")
        last_name = request.data.get("last_name")
        email = request.data.get("email")
        nickname = request.data.get("nickname")
        date_of_birth = request.data.get("date_of_birth")


        User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            email=email,
            nickname=nickname,
            date_of_birth=date_of_birth,
        )

        return Response({})
