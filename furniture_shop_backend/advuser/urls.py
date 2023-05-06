from django.urls import path

from advuser.views import (EmailLoginView, LogoutView, 
                           SignupView, RegisterDoneView, user_activate,
                           ChangePasswordView, ChangePasswordDoneView,
                           UpdateUserView, UpdateUserDoneView)

app_name = "auth"

urlpatterns = [
    path("login/", EmailLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/activate/<str:sign>/", user_activate, name="register_activate"),
    path("register/successful/", RegisterDoneView.as_view(), name="register_done"),
    path("register/", SignupView.as_view(), name="signup"),
    path("password/change/done/", ChangePasswordDoneView.as_view(), name="password_change_done"),
    path("password/change/", ChangePasswordView.as_view(), name="password_change"),
    path("update/done/", UpdateUserDoneView.as_view(), name="update_done"),
    path("update/", UpdateUserView.as_view(), name="update"),
]