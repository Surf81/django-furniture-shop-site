import json
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse, reverse_lazy

from advuser.models import AdvancedUser
from main.models import Product, SuperCategory, SubCategory, Comment
from api.serializers import ProductSerializer, CommentSerializer

# Create your tests here.
class ProductAPITestCase(APITestCase):
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


class CommentAPITestCase(APITestCase):
    def setUp(self):
        self.user = AdvancedUser.objects.create(email="admin@admin.net", password='ABC102030')

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
        
        self.comment1 = Comment.objects.create(product=self.product1, author='anonim', content='Comment 1')
        self.comment2 = Comment.objects.create(product=self.product2, author='anonim1', content='Comment 2')
        self.comment3 = Comment.objects.create(product=self.product2, author='anonim2', content='Comment 3', is_active=False)


    def test_get(self):
        url = reverse('api:comment')
        response = self.client.get(url)
        serializer_data = CommentSerializer([self.comment1, self.comment2], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)


    def test_post_not_authenticate(self):
        url = reverse('api:comment')
        response = self.client.post(url, 
                         {
                            'product': self.product1.pk,
                            'author': 'unknown',
                            'content': 'Comment 4',
                         }, 
                         format='json')
        
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)


    def test_post(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('api:comment')
        response = self.client.post(url, 
                         {
                            'product': self.product1.pk,
                            'author': 'unknown',
                            'content': 'Comment 4',
                         }, 
                         format='json')
        
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)


    def test_post_wrong(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('api:comment')
        response = self.client.post(url, 
                         {
                            'product': 1,
                            'content': 50,
                         }, 
                         format='json')

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)


