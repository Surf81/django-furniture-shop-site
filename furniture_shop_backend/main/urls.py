from django.urls import include, path

from main.views import any_page, IndexPageView, DetailPageView

app_name = "main"

urlpatterns = [
    path("<str:url>/", any_page, name="any_page"),
    path("detail/<int:pk>/", DetailPageView.as_view(), name="detail"),
    path("", IndexPageView.as_view(), name="index"),
]