from .models import Product, CharacteristicItem
from rest_framework import serializers


class CharacteristicItemSerializer(serializers.ModelSerializer):
    group_id = serializers.IntegerField(source='group.id')
    group_title = serializers.CharField(source='group.title')
    class Meta:
        model = CharacteristicItem
        fields = ('id', 'title', 'group_id', 'group_title')


class ProductSerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField(source='category.id')
    category_name = serializers.CharField(source='category.title')
    characteristics = CharacteristicItemSerializer(many=True)
    class Meta:
        model = Product
        fields = ('id', 'title', 'description', 'count', 'price', 'image', 
                  'created_at', 'changed_at', 'category_id', 'category_name', 'characteristics')
