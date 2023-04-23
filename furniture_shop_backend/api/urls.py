from django.urls import path
from rest_framework.routers import SimpleRouter
from .views import ProductViewSet, ProductDetailView, comments

router = SimpleRouter()
router.register(r'store', ProductViewSet)

app_name = "api"

urlpatterns = [
    *router.urls,
    path('detail/<int:pk>/comments/', comments),
    path('detail/<int:pk>/', ProductDetailView.as_view()),
]

