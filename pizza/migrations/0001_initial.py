# Generated by Django 3.0 on 2019-12-06 13:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_name', models.CharField(max_length=50)),
                ('customer_email', models.EmailField(max_length=254)),
                ('customer_phone', models.CharField(max_length=13, verbose_name='Customer`s phone number')),
                ('customer_comment', models.TextField(blank=True, max_length=1000, verbose_name='Client provided info')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=5, null=True, verbose_name='Order amount')),
                ('paid', models.BooleanField(default=False, verbose_name='Order is paid')),
                ('status', models.IntegerField(choices=[(0, 'NEW'), (1, 'CONFIRMED'), (2, 'SENT_TO_DELIVERY'), (3, 'ON_THE_WAY'), (4, 'DELIVERED'), (10, 'DECLINED')], default=0, verbose_name='Order status')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Pizza',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('description', models.TextField(blank=True, max_length=1000, verbose_name='Description')),
            ],
        ),
        migrations.CreateModel(
            name='PizzaPrice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(choices=[('small', 'small'), ('medium', 'medium'), ('large', 'large')], max_length=10)),
                ('price', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Price of this pizza size')),
                ('pizza', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prices', to='pizza.Pizza')),
            ],
            options={
                'unique_together': {('size', 'pizza')},
            },
        ),
        migrations.CreateModel(
            name='OrderedPizza',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.PositiveIntegerField(default=0, verbose_name='Count of pizzas')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ordered_pizzas', to='pizza.Order')),
                ('pizza_price', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ordered_pizzas', to='pizza.PizzaPrice')),
            ],
            options={
                'unique_together': {('pizza_price', 'order')},
            },
        ),
    ]
