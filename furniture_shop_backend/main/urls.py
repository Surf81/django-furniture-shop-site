from django.urls import include, path

from main.views import any_page, IndexPageView, DetailPageView, CategoryPageView

app_name = "main"

urlpatterns = [
    path("<str:url>/", any_page, name="any_page"),
    path("detail/<int:pk>/", DetailPageView.as_view(), name="detail"),
    path("category/<int:pk>/", CategoryPageView.as_view(), name="category"),
    path("", IndexPageView.as_view(), name="index"),
]