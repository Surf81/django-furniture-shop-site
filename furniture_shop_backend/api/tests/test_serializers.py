from django.test import TestCase
from django.urls import reverse

from main.models import Product, SuperCategory, SubCategory
from api.serializers import ProductSerializer

# Create your tests here.
class ProductSerializerTestCase(TestCase):
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

    def test_serializer(self):
        serializer_data = ProductSerializer([self.product1, self.product2], many=True).data
        expected_data = [
            {
                'id': self.product1.pk,
                'title': "Диван 1",
                'description': 'Хороший диван',
                'count': 1,
                'price': 10000,
                'image': None,
                'category_id': self.category2.pk,
                'category_name': 'Обычный диван',
                'characteristics': [],
            },
            {
                'id': self.product2.pk,
                'title': "Диван 2",
                'description': 'Очень хороший диван',
                'count': 1,
                'price': 100000,
                'image': None,
                'category_id': self.category1.pk,
                'category_name': 'VIP диван',
                'characteristics': [],
            },
        ]
        self.assertEqual(expected_data, serializer_data)
        
