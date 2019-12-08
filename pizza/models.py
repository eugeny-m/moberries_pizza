from decimal import Decimal

from django.db import models

from pizza import const


class Pizza(models.Model):

    name = models.CharField('Name', max_length=50, blank=False)
    description = models.TextField('Description', max_length=1000, blank=True)

    def __str__(self):
        return f'ID {self.id}: {self.name}'


class PizzaPrice(models.Model):
    """Model for pizza size and price storage"""

    pizza = models.ForeignKey(
        'pizza.Pizza',
        related_name='prices',
        null=False,
        blank=False,
        on_delete=models.CASCADE,
    )
    size = models.CharField(
        choices=const.PIZZA_SIZES,
        max_length=10,
        null=False,
        blank=False,
    )
    price = models.DecimalField(
        'Price of this pizza size',
        max_digits=5,
        decimal_places=2,
        null=False,
        blank=False,
    )

    def __str__(self):
        return f'{self.pizza.name} - {self.size}'

    class Meta:
        unique_together = ('size', 'pizza')


class Order(models.Model):

    customer_name = models.CharField(max_length=50, blank=False)
    customer_email = models.EmailField(null=False, blank=False)
    customer_phone = models.CharField(
        'Customer`s phone number',
        max_length=13,
        blank=False
    )
    customer_comment = models.TextField(
        'Client provided info',
        max_length=1000,
        blank=True
    )

    amount = models.DecimalField(
        'Order amount',
        decimal_places=2,
        max_digits=5,
        null=True)
    paid = models.BooleanField('Order is paid', default=False)
    status = models.IntegerField(
        'Order status',
        choices=const.ORDER_STATUSES,
        default=const.NEW,
    )
    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True)

    def get_amount(self) -> Decimal:
        result = sum([op.get_amount() for op in self.ordered_pizzas.all()])
        return result

    def update_amount(self):
        if self.status == const.NEW:
            self.amount = self.get_amount()
            self.save()


class OrderedPizza(models.Model):
    """
    Model for storing Order positions
    """
    pizza_price = models.ForeignKey(
        to='pizza.PizzaPrice',
        related_name='ordered_pizzas',
        null=True,
        on_delete=models.SET_NULL,
    )
    order = models.ForeignKey(
        to='pizza.Order',
        related_name='ordered_pizzas',
        null=False,
        on_delete=models.CASCADE
    )
    count = models.PositiveIntegerField('Count of pizzas', default=0)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('pizza_price', 'order')

    def get_amount(self) -> Decimal:
        return self.pizza_price.price * self.count

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.order.update_amount()

    def delete(self, using=None, keep_parents=False):
        order = self.order
        res = super().delete(using, keep_parents)
        order.update_amount()
        return res
