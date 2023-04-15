from django.urls import path

from advuser.views import (EmailLoginView, LogoutView, SignupView, RegisterDoneView, 
                           ChangePasswordView, ChangePasswordDoneView, 
                           UpdateUserView, UpdateUserDoneView)

app_name = "auth"

urlpatterns = [
    path("login/", EmailLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("signup/successful/", RegisterDoneView.as_view(), name="register_done"),
    path("signup/", SignupView.as_view(), name="signup"),
    path("password/change/done/", ChangePasswordDoneView.as_view(), name="password_change_done"),
    path("password/change/<int:pk>/", ChangePasswordView.as_view(), name="password_change"),
    path("update/done/", UpdateUserDoneView.as_view(), name="update_done"),
    path("update/<int:pk>/", UpdateUserView.as_view(), name="update"),
]