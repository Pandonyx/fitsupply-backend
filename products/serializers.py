from rest_framework import serializers
from .models import Category, Product

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description']

class ProductSerializer(serializers.ModelSerializer):
    # Use StringRelatedField to show the category name instead of its ID
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'category', 'category_name', 'short_description', 'price',
            'compare_price', 'stock_quantity', 'is_featured', 'is_active', 'image'
        ]
        extra_kwargs = {
            'category': {'write_only': True}
        }