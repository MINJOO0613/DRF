from django.urls import path
from . import views
from rest_framework_simplejwt.views import(
    TokenObtainPairView,
    TokenRefreshView
)


app_name = "accounts"
urlpatterns = [
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"), # refresh_token 발행
    path("", views.SignupView.as_view(), name="sign_up_view"), # 회원가입 및 token 발행
    path("login/", views.LoginView.as_view(), name="log_in_view"), # 로그인 및 token 발행
    path("logout/", views.LogoutView.as_view(), name="log_out_view"), # 로그아웃 및 refresh_token 블랙리스트 처리
    path("password/", views.PasswordChangeView.as_view(), name="password_change_view"), # 패스워드 변경
    path("<str:username>/", views.ProfileView.as_view(), name="profile_view"), # 프로필 조회 및 회원정보 수정
    path('<str:username>/follow/', views.FollowAPI.as_view(), name="follow"), #팔로우/팔로워
]