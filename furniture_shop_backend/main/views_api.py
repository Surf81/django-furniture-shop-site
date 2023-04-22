from django.db.models import BooleanField
from django.db.models import Case, When
from rest_framework import viewsets

from .models import Product
from .serializers import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(is_active__exact=True)
    serializer_class = ProductSerializer
