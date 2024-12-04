from rest_framework import serializers
from .models import Restaurant, RestaurantEmployee, Category, Item, Modifier


class ModifierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Modifier
        fields = ['id', 'name', 'price', 'item']

class ItemSerializer(serializers.ModelSerializer):
    modifiers = ModifierSerializer(many=True, read_only=True)
    class Meta:
        model = Item
        fields = ['id', 'name','description', 'price', 'menu_category','modifiers']

class CategorySerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'restaurant' ,'items']



class RestaurantSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'location', 'owner', 'categories']
        read_only_fields = ['id', 'owner',]


class RestaurantEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantEmployee
        fields = ['id', 'employee', 'restaurant']
        read_only_fields = ['id']