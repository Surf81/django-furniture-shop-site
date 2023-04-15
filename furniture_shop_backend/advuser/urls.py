from django.urls import include, path

from advuser.views import EmailLoginView, SignupView

app_name = "auth"

urlpatterns = [
    path("login/", EmailLoginView.as_view(), name="login"),
]