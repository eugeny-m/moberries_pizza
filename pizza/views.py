from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied

from pizza import const
from pizza.models import Pizza, Order, OrderedPizza, PizzaPrice
from pizza.serializers import (
    OrderSerializer,
    OrderedPizzaSerializer,
    PizzaSerializer,
    PizzaPriceSerializer)


class PizzaViewSet(viewsets.ModelViewSet):
    serializer_class = PizzaSerializer
    queryset = Pizza.objects.all()


class PizzaPriceViewSet(viewsets.ModelViewSet):
    serializer_class = PizzaPriceSerializer
    queryset = PizzaPrice.objects.all()

    def destroy(self, request, *args, **kwargs):
        """
        method overridden to protect from removing PizzaPrice objects,
        selected in new orders.
        (It is political problem, here is just one of possible realizations)
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        instance = self.get_object()
        new_orders_exists = Order.objects.filter(
            status=const.NEW,
            ordered_pizzas__pizza_price=instance
        ).exists()
        if new_orders_exists:
            error_msg = "You can't delete PizzaPrice " \
                        "while it related to a new Order!"
            raise PermissionDenied(error_msg)

        return super().destroy(request, *args, **kwargs)


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()


class OrderedPizzaViewSet(viewsets.ModelViewSet):
    serializer_class = OrderedPizzaSerializer
    queryset = OrderedPizza.objects.all()
