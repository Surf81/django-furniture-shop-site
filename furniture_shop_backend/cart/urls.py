from django.urls import include, path

from cart.views import cart_add, cart_view, cart_sub, cart_del, cart_clear

app_name = "cart"

urlpatterns = [
    path("add/<int:pk>/", cart_add, name="cart_add"),
    path("sub/<int:pk>/", cart_sub, name="cart_sub"),
    path("del/<int:pk>/", cart_del, name="cart_del"),
    path("clear/", cart_clear, name="cart_clear"),
    path("", cart_view, name="cart_view"),
]