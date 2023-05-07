from django.urls import path
from rest_framework.routers import SimpleRouter
from .views import ProductViewSet, ProductMoreDetailView, comment_CR_api

router = SimpleRouter()
router.register(r'store', ProductViewSet, basename='store')

app_name = "api"

urlpatterns = [
    *router.urls,
    path('comment/', comment_CR_api, name='comment'),
    path('detail/<int:pk>/', ProductMoreDetailView.as_view()),
]

