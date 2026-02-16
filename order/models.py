from django.contrib.auth.models import User
from django.db import models

from order.choices import ORDER_STATUS


class Order(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    counter_party = models.ForeignKey('counter_party.CounterParty',
                                      verbose_name='Агент',
                                      on_delete=models.PROTECT)
    status = models.SmallIntegerField(default=0,
                                      verbose_name='Статус', choices=ORDER_STATUS)
    user = models.ForeignKey(User,
                             on_delete=models.PROTECT,
                             verbose_name='Пользователь')
    total_uzs = models.FloatField(default=0,
                                  verbose_name='Итоговая сумма (uzs)')
    total_usd = models.FloatField(default=0,
                                  verbose_name='Итоговая сумма (usd)')
    rate = models.FloatField(default=0,
                             verbose_name='Курс валюты')

    def __str__(self):
        return self.counter_party.name


class OrderItem(models.Model):
    product = models.ForeignKey('product.Product',
                                verbose_name='Продукт',
                                related_name='order_item',
                                on_delete=models.PROTECT)
    count = models.FloatField(default=0,
                              verbose_name='Количество (кг)')
    price = models.FloatField(default=0,
                              verbose_name='Цена')
    status = models.SmallIntegerField(default=0,
                                      verbose_name='Статус')
    order = models.ForeignKey('Order',
                              on_delete=models.CASCADE,
                              verbose_name='Заказ')
    total_uzs = models.FloatField(default=0)
    total_usd = models.FloatField(default=0)
    rate = models.FloatField(default=0,
                             verbose_name='Курс валюты')

    def __str__(self):
        return str(self.pk)


class OrderReturnItem(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    count = models.FloatField(default=0,
                              verbose_name='Количество (кг)')
    status = models.SmallIntegerField(default=0,
                                      verbose_name='Статус')
    order_item = models.ForeignKey('OrderItem',
                                   on_delete=models.CASCADE,
                                   verbose_name='Продукт')
    total_uzs = models.FloatField(default=0)
    total_usd = models.FloatField(default=0)
    rate = models.FloatField(default=0,
                             verbose_name='Курс валюты')

    def __str__(self):
        return str(self.pk)