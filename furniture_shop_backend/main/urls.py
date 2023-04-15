from django.urls import include, path

from main.views import any_page, index

app_name = "main"

urlpatterns = [
    path("<str:url>/", any_page, name="any_page"),
    path("", index, name="index"),
]