from django.urls import path

from advuser.views import EmailLoginView, SignupView, RegisterDoneView

app_name = "auth"

urlpatterns = [
    path("login/", EmailLoginView.as_view(), name="login"),
    path("signup/successful/", RegisterDoneView.as_view(), name="register_done"),
    path("signup/", SignupView.as_view(), name="signup"),
]