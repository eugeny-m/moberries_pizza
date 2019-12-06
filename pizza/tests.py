from decimal import Decimal, ROUND_05UP
from django.test import TestCase
from django.urls import reverse

from rest_framework import status

from pizza import const
from pizza.models import PizzaPrice, Order, OrderedPizza


class PizzaTest(TestCase):

    def test_post_pizza(self):
        resp = self.client.post(
            path=reverse('pizza-list'),
            data={'name': 'Pizza1'}
        )
        self.assertEquals(resp.status_code, status.HTTP_201_CREATED)


class OrderTest(TestCase):
    ORDER_POST_DATA = {
        'customer_name': 'customer_1',
        'customer_phone': '1234567810',
        'customer_email': 'customer_1@example.com',
    }

    def test_post_order(self):
        resp = self.client.post(
            path=reverse('order-list'),
            data=self.ORDER_POST_DATA,
        )
        self.assertEquals(resp.status_code, status.HTTP_201_CREATED)


class OrderedPizzaTest(TestCase):
    """
    TestCase for testing OrderedPizza endpoints
    """

    fixtures = [
        'pizza/fixtures/pizza_fixtures.yaml',
        'pizza/fixtures/order_fixtures.yaml',
    ]

    def test_post_orderedpizza(self):
        order = Order.objects.get(id=1)
        self.assertEquals(order.amount, None)

        # testing add pizza to order
        price = PizzaPrice.objects.get(id=1)
        resp = self.client.post(
            path=reverse('orderedpizza-list'),
            data={
                'count': 1,
                'pizza_price': price.id,
                'order': order.id,
            }
        )
        self.assertEquals(resp.status_code, status.HTTP_201_CREATED)

        # testing order amount updating
        order.refresh_from_db()
        self.assertEquals(order.amount, price.price)

    def test_patch_orderedpizza_new_order(self):
        op = OrderedPizza.objects.get(id=1)
        resp = self.client.patch(
            path=reverse('orderedpizza-detail', args=[op.id]),
            data={'count': op.count * 2},
            content_type='application/json'
        )
        self.assertEquals(resp.status_code, status.HTTP_200_OK)

        # testing order amount updating
        order = op.order
        self.assertEquals(order.amount, op.pizza_price.price * 2)

    def test_patch_orderedpizza_not_new_order(self):
        """test patching order position for order with any status except NEW"""
        op = OrderedPizza.objects.get(id=1)
        for status_, verbal in const.ORDER_STATUSES:
            if status_ == const.NEW:
                continue
            Order.objects.filter(id=op.order_id).update(status=status_)

            resp = self.client.patch(
                path=reverse('orderedpizza-detail', args=[op.id]),
                data={'count': op.count * 2},
                content_type='application/json'
            )
            self.assertEquals(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_destroy_orderedpizza_new_order(self):
        op = OrderedPizza.objects.get(id=1)
        order = op.order

        resp = self.client.delete(
            path=reverse('orderedpizza-detail', args=[op.id]),
        )
        self.assertEquals(resp.status_code, status.HTTP_204_NO_CONTENT)

        # testing order amount updating
        order.refresh_from_db()
        self.assertEquals(order.amount, Decimal('0.00'))

    def test_destroy_orderedpizza_not_new_order(self):
        """test delete order position for order with any status except NEW"""
        op = OrderedPizza.objects.get(id=1)
        for status_, verbal in const.ORDER_STATUSES:
            if status_ == const.NEW:
                continue
            Order.objects.filter(id=op.order_id).update(status=status_)
            resp = self.client.delete(
                path=reverse('orderedpizza-detail', args=[op.id]),
            )
            self.assertEquals(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_orderedpizza_non_defined_fields(self):
        # patch shouldn't update fields that not defined in update serializer
        op = OrderedPizza.objects.get(id=1)
        resp = self.client.patch(
            path=reverse('orderedpizza-detail', args=[op.id]),
            data={'count': op.count * 2, 'order': 100},
            content_type='application/json'
        )
        op.refresh_from_db()
        self.assertFalse('order' in resp.json())
