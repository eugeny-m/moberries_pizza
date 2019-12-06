from typing import Any

from django.db.models import Model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from pizza import const
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

    def update(self, instance, validated_data):
        if instance.order.status != const.NEW:
            raise ValidationError("You can't change order after confirmation!")
        return super().update(instance, validated_data)

    def create(self, validated_data):
        order = validated_data['order']
        if order.status != const.NEW:
            raise ValidationError("You can't change order after confirmation!")
        return super().create(validated_data)


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

    def update(self, instance: Model, validated_data: Any) -> Any:
        return super().update(instance, validated_data)
