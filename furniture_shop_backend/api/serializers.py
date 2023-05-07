from main.models import Product, CharacteristicItem, Comment
from rest_framework import serializers


class CharacteristicItemSerializer(serializers.ModelSerializer):
    group_id = serializers.IntegerField(source='group.id')
    group_title = serializers.CharField(source='group.title')
    class Meta:
        model = CharacteristicItem
        fields = ('id', 'title', 'group_id', 'group_title')


class ProductSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    # category_id = serializers.IntegerField(source='category.id')
    category_name = serializers.ReadOnlyField(source='category.title')
    characteristics = CharacteristicItemSerializer(many=True, read_only=True)
    class Meta:
        model = Product
        fields = ('id', 'title', 'description', 'count', 'price', 'image', 
                  'category', 'category_name', 'characteristics')


class ProductDetailSerializer(ProductSerializer):
    class Meta:
        model = Product
        fields = ('id', 'title', 'description', 'count', 'price', 'image', 
                  'created_at', 'changed_at', 
                  'category_id', 'category_name', 'characteristics')

        
class CommentSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    created_at = serializers.ReadOnlyField()
    class Meta:
        model = Comment
        fields = ('id', 'product', 'author', 'content', 'created_at')        