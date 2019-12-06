import django_filters

from rest_framework import viewsets, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from pizza import const
from pizza.models import Pizza, Order, OrderedPizza, PizzaPrice
from pizza.serializers import (
    OrderSerializer,
    OrderedPizzaSerializer,
    PizzaSerializer,
    PizzaPriceSerializer,
    OrderUpdateSerializer,
    OrderedPizzaUpdateSerializer
)


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
        in_process_orders_exists = Order.objects.filter(
            status__lt=const.DELIVERED,
            ordered_pizzas__pizza_price=instance
        ).exists()
        if in_process_orders_exists:
            raise PermissionDenied("You can't delete PizzaPrice while it "
                                   "related to a new Order!")

        return super().destroy(request, *args, **kwargs)


class OrderFilter(django_filters.FilterSet):
    class Meta:
        model = Order
        fields = {
            'customer_email': ['exact', 'in'],
            'status': ['exact', 'in'],
        }


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    filter_class = OrderFilter

    def get_serializer_class(self):
        if self.action in ('update', 'partial_update'):
            return OrderUpdateSerializer
        return self.serializer_class


def check_order_is_mutable(order):
    """
    Function raises PermissionDenied exception
    if order status is not const.NEW
    """
    if order.status != const.NEW:
        raise PermissionDenied("You can't change order positions "
                               "after confirmation!")


class OrderedPizzaViewSet(viewsets.ModelViewSet):
    serializer_class = OrderedPizzaSerializer
    queryset = OrderedPizza.objects.all()

    def get_serializer_class(self):
        if self.action in ('update', 'partial_update'):
            return OrderedPizzaUpdateSerializer
        return self.serializer_class

    def destroy(self, request, *args, **kwargs):
        order = self.get_object().order
        check_order_is_mutable(order)
        return super().destroy(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        order = self.get_object().order
        check_order_is_mutable(order)
        return super().update(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.validated_data['order']
        check_order_is_mutable(order)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers)
