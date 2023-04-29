from django.test import TestCase
from django.urls import reverse

from advuser.models import AdvancedUser
from main.models import (Product, 
                         SuperCategory, 
                         SubCategory, 
                         CharacteristicGroup, 
                         CharacteristicItem,
                         Comment,
                         CharacteristicProductRelated
                        )
from api.serializers import (CharacteristicItemSerializer,
                             ProductSerializer,
                             ProductDetailSerializer,
                             CommentSerializer
                             )


class CharacteristicItemSerializerTestCase(TestCase):
    def setUp(self):
        self.characteristic_group1 = CharacteristicGroup.objects.create(title="Цвет")
        self.characteristic1 = CharacteristicItem.objects.create(title="Белый", 
                                                                 group=self.characteristic_group1,
                                                                 type = CharacteristicItem.Types.SELECT)
        self.characteristic2 = CharacteristicItem.objects.create(title="Черный", 
                                                                 group=self.characteristic_group1,
                                                                 type = CharacteristicItem.Types.SELECT)

        self.characteristic_group2 = CharacteristicGroup.objects.create(title="Вес")
        self.characteristic3 = CharacteristicItem.objects.create(title="кг", 
                                                                 group=self.characteristic_group2,
                                                                 type = CharacteristicItem.Types.VALUE)


    def test_serializer(self):
        serializer_data = CharacteristicItemSerializer([self.characteristic1, self.characteristic2, self.characteristic3], many=True).data
        expected_data = [
            {
                'id': self.characteristic1.pk,
                'title': "Белый",
                'group_id': self.characteristic_group1.pk,
                'group_title': 'Цвет',
            },
            {
                'id': self.characteristic2.pk,
                'title': "Черный",
                'group_id': self.characteristic_group1.pk,
                'group_title': 'Цвет',
            },
            {
                'id': self.characteristic3.pk,
                'title': "кг",
                'group_id': self.characteristic_group2.pk,
                'group_title': 'Вес',
            },
        ]
        self.assertEqual(expected_data, serializer_data)


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
        

class ProductDetailSerializerTestCase(TestCase):
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
        serializer_data = ProductDetailSerializer([self.product1, self.product2], many=True).data

        for data in serializer_data:
            del data['created_at']
            del data['changed_at']

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
        

class CommentSerializerTestCase(TestCase):
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
        
        self.comment1 = Comment.objects.create(product=self.product1, author='anonim', content='Comment 1')
        self.comment2 = Comment.objects.create(product=self.product2, author='anonim1', content='Comment 2')
        self.comment3 = Comment.objects.create(product=self.product2, author='anonim2', content='Comment 3')

    def test_serializer(self):
        serializer_data = CommentSerializer([self.comment1, self.comment2, self.comment3], many=True).data

        for data in serializer_data:
            del data['created_at']

        expected_data = [
            {
                'id': self.comment1.pk,
                'product': self.product1.pk,
                'author': 'anonim',
                'content': 'Comment 1',
            },
            {
                'id': self.comment2.pk,
                'product': self.product2.pk,
                'author': 'anonim1',
                'content': 'Comment 2',
            },
            {
                'id': self.comment3.pk,
                'product': self.product2.pk,
                'author': 'anonim2',
                'content': 'Comment 3',
            },
        ]
        self.assertEqual(expected_data, serializer_data)
        
