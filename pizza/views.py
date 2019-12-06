from rest_framework import viewsets, mixins

from pizza.models import Pizza, Order, OrderedPizza
from pizza.serializers import (
    OrderSerializer,
    OrderedPizzaSerializer,
    PizzaSerializer,
    PizzaPriceSerializer)


class PizzaViewSet(viewsets.ModelViewSet):
    serializer_class = PizzaSerializer
    queryset = Pizza.objects.all()


class PizzaPriceViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin
):
    serializer_class = PizzaPriceSerializer
    queryset = Pizza.objects.all()


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()


class OrderedPizzaViewSet(viewsets.ModelViewSet):
    serializer_class = OrderedPizzaSerializer
    queryset = OrderedPizza.objects.all()
