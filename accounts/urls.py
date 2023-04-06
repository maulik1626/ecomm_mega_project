from django.urls import path
from accounts.views import *


urlpatterns = [
    path("register/", register, name="register"),
    path("login/", login, name="login"),
    path("logout/", logout, name="logout"),
    
    path("activate/<uidb64>/<token>/", activate, name="activate"),

    path("dashboard/", dashboard, name="dashboard"),
    path("forgot_password/", forgot_password, name="forgot_password"),

    path("reset_password_validate/<uidb64>/<token>/", reset_password_validate, name="reset_password_validate"),
    path("reset_password/", reset_password, name="reset_password"),
]