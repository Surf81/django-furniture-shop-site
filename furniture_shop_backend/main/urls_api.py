from rest_framework.routers import SimpleRouter

from .views_api import ProductViewSet


router = SimpleRouter()
router.register(r'store', ProductViewSet)


app_name = "api"

urlpatterns = [
    *router.urls,
]

