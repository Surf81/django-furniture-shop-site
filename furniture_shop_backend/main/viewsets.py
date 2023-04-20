from django.db.models import BooleanField
from django.db.models import Case, When
from rest_framework import viewsets

from .models import Product
from .serializers import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return (super().get_queryset()
                           .annotate(favorite=Case(
                               When(id__in=self.request.user.userproductrelated_set.filter(is_favorit__exact=True).values('product__id'), then=True),
                                default=False,
                                output_field=BooleanField()
                          ))
            )
        return super().get_queryset()
