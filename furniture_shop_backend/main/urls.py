from django.urls import include, path

from .views import (any_page, IndexPageView, DetailPageView, 
                        CategoryPageView, 
                        favorite_toggle, FavoriteProductsView,
                        product_create_view,
                        product_edit_view,
                        product_del_view)


app_name = "main"

urlpatterns = [
    path("product/<int:pk>/", DetailPageView.as_view(), name="detail"),
    path("category/<int:pk>/", CategoryPageView.as_view(), name="category"),
    path("add/", product_create_view, name="product_create"),
    path("edit/<int:pk>/", product_edit_view, name="product_edit"),
    path("delete/<int:pk>/", product_del_view, name="product_delete"),
    path("favorite/<int:pk>/", favorite_toggle, name="favorite_toggle"),
    path("favorite/", FavoriteProductsView.as_view(), name="favorite_products"),
    path("<str:url>/", any_page, name="any_page"),
    path("", IndexPageView.as_view(), name="index"),
]

