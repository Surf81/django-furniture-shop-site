from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse

from main.models import Product, SuperCategory, SubCategory
from api.serializers import ProductSerializer

# Create your tests here.
class MainAPITestCase(APITestCase):
    def setUp(self):
        super_category = SuperCategory.objects.create(title="Диваны")
        self.category1 = SubCategory.objects.create(title="VIP диван", super_category=super_category)
        self.category2 = SubCategory.objects.create(title="Обычный диван", super_category=super_category)


        self.product1 = Product.objects.create(title="Диван 1", 
                                               description="Хороший диван",
                                               count=1,
                                               price=10000,
                                               category=self.category2)
        self.product2 = Product.objects.create(title="Диван 2", 
                                               description="Очень хороший диван",
                                               count=1,
                                               price=100000,
                                               category=self.category1)

    def test_get(self):
        url = reverse('api:product-list')
        response = self.client.get(url)
        serializer_data = ProductSerializer([self.product1, self.product2], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)
