from rest_framework import serializers
from pizza.models import Pizza, PizzaPrice, Order, OrderedPizza


class PizzaPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PizzaPrice
        fields = '__all__'


class PizzaSerializer(serializers.ModelSerializer):
    prices = PizzaPriceSerializer(many=True, read_only=True)

    class Meta:
        model = Pizza
        fields = ('id', 'name', 'description', 'prices')


class OrderedPizzaSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderedPizza
        fields = '__all__'


class OrderedPizzaUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderedPizza
        fields = ['count']


class OrderSerializer(serializers.ModelSerializer):
    ordered_pizzas = OrderedPizzaSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['amount']


class OrderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status', 'paid']
