from django.urls import path
from . import views
from rest_framework_simplejwt.views import(
    TokenObtainPairView,
    TokenRefreshView
)


app_name = "accounts"
urlpatterns = [
    # path("signin/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("", views.SignupView.as_view(), name="sign_up_view"),
    path("login/", views.LoginView.as_view(), name="log_in_view"),
    path("logout/", views.LogoutView.as_view(), name="log_out_view"),
    path("password/<str:username>/", views.PasswordView.as_view(), name="password_view"),
    path("<str:username>/", views.ProfileView.as_view(), name="profile_view"),
]