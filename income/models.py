from django.db import models
from django.contrib.auth.models import User
from income.choices import INCOME_STATUS


class Income(models.Model):
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    total_uzs = models.FloatField(default=0, verbose_name='Сумма(uzs)')
    total_usd = models.FloatField(default=0, verbose_name='Сумма(usd)')
    status = models.BigIntegerField(default=0, choices=INCOME_STATUS, verbose_name='статус')
    counter_party = models.ForeignKey('counter_party.CounterParty',
                                      on_delete=models.PROTECT,
                                      verbose_name='Агент')
    user = models.ForeignKey(User,
                             on_delete=models.PROTECT,
                             verbose_name='Пользователь')
    rate = models.FloatField(verbose_name='Курс доллара тогда',
                             default=0, null=True, blank=True)

    def __str__(self):
        return self.counter_party.name


class IncomeItem(models.Model):
    product = models.ForeignKey('product.Product',
                                on_delete=models.PROTECT,
                                verbose_name='Продукты')
    count = models.FloatField(default=0,
                              verbose_name='Количество')
    total_uzs = models.FloatField(default=0, verbose_name='Сумма(uzs)')
    total_usd = models.FloatField(default=0, verbose_name='Сумма(usd)')
    price = models.FloatField(default=0,
                              verbose_name='Цена')
    income = models.ForeignKey('Income', on_delete=models.CASCADE)
    currency = models.CharField(verbose_name='Валюта', default='usd',
                                max_length=10)

    def __str__(self):
        return str(self.product)
