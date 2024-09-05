from django.urls import path
from . import views
from rest_framework_simplejwt.views import(
    TokenObtainPairView,
    TokenRefreshView
)


app_name = "accounts"
urlpatterns = [
    # path("signin/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    # path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    path("signup/", views.SignupView.as_view(), name="sign_up_view"),
    path("login/", views.LoginView.as_view(), name="log_in_view"),
]