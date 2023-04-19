from django.urls import include, path

from main.views import (any_page, IndexPageView, DetailPageView, 
                        CategoryPageView, 
                        favorite_toggle, FavoriteProductsView)

app_name = "main"

urlpatterns = [
    path("detail/<int:pk>/", DetailPageView.as_view(), name="detail"),
    path("category/<int:pk>/", CategoryPageView.as_view(), name="category"),
    path("favorite/<int:pk>/", favorite_toggle, name="favorite_toggle"),
    path("favorite/", FavoriteProductsView.as_view(), name="favorite_products"),
    path("<str:url>/", any_page, name="any_page"),
    path("", IndexPageView.as_view(), name="index"),
]