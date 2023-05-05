from rest_framework import serializers
from django.contrib.auth.models import User, Group
from .models import Category,MenuItem,Cart,Order,OrderItem


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'title', 'slug']
        
class MenuItemSerializer(serializers.HyperlinkedModelSerializer):
    category_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'featured', 'category_id'] 
        read_only_fields = ['category']
        
    def create(self, validated_data):
        category_id = validated_data.pop('category_id')
        category = Category.objects.get(id=category_id)
        menu_item = MenuItem.objects.create(category=category, **validated_data)
        return menu_item
        
class CartSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Cart
        fields = ['id', 'user', 'menuitem', 'quantity', 'unit_price', 'price']
        read_only = ['user', 'unit_price', 'price']

class OrderItemSerializer(serializers.HyperlinkedModelSerializer):
        
    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'menuitem', 'quantity', 'unit_price', 'price']
        read_only_fields = ['order', 'unit_price', 'price']

class OrderSerializer(serializers.HyperlinkedModelSerializer):
    order_items = OrderItemSerializer(many=True) #Is this necessary? Seems like it...
    
    class Meta:
        model = Order
        fields = ['id', 'user', 'delivery_crew', 'status', 'total', 'date', 'order_items'] # Is this necessary? Seems like it...
        read_only = ['id', 'user', 'delivery_crew', 'total', 'date']
        extra_kwargs = {'delivery_crew_id': {'write_only': True}}


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ['id', 'name']