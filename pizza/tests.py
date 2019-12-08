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
        'customer_email': '1@example.com',
    }

    fixtures = [
        'pizza/fixtures/pizza_fixtures.yaml',
        'pizza/fixtures/order_fixtures.yaml',
    ]

    # filter_name -- filter value -- expected result(order_id)
    FILTERS_PARAMS = (
        ('customer_email', '1@example.com', [1, 2]),
        ('customer_email__in', '1@example.com', [1, 2]),
        ('customer_email__in', '1@example.com,non@example.com', [1, 2]),
        ('customer_email__in', '1@example.com,2@example.com', [1, 2, 3]),
        ('status', 0, [1, 2]),
        ('status__in', '0', [1, 2]),
        ('status__in', '0,3', [1, 2, 3, 4]),
        ('status__in', '1,3', [3, 4]),
    )

    def test_post_order(self):
        resp = self.client.post(
            path=reverse('order-list'),
            data=self.ORDER_POST_DATA,
        )
        self.assertEquals(resp.status_code, status.HTTP_201_CREATED)

    def test_destroy_order(self):
        order = Order.objects.get(id=1)
        resp = self.client.delete(
            path=reverse('order-detail', args=[order.id]),
        )
        self.assertEquals(resp.status_code, status.HTTP_204_NO_CONTENT)

    def test_order_list_filters(self):

        # single-using filters
        for f_name, f_value, f_result in self.FILTERS_PARAMS:
            resp = self.client.get(
                reverse('order-list'),
                {f_name: f_value}
            )
            with self.subTest(f'{f_name}: {f_value}'):
                self.assertEquals(f_result, [o['id'] for o in resp.json()])

        # multiple-using
        resp = self.client.get(
            reverse('order-list'),
            {'customer_email': '1@example.com', 'status': 0}
        )
        self.assertEquals([1,2], [o['id'] for o in resp.json()])

        resp = self.client.get(
            reverse('order-list'),
            {'customer_email': '1@example.com', 'status': 1}
        )
        self.assertEquals([], [o['id'] for o in resp.json()])


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

        # test for Order - PizzaPrice uniqness
        resp = self.client.post(
            path=reverse('orderedpizza-list'),
            data={
                'count': 2,
                'pizza_price': price.id,
                'order': order.id,
            }
        )
        self.assertEquals(resp.status_code, status.HTTP_400_BAD_REQUEST)

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
