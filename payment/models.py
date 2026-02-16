from django.contrib.auth.models import User
from django.db import models

from payment.choices import OUTLAY_TYPE_CHOICES, AMOUNT_TYPE_CHOICES, PAYMENT_LOG_OUTLAY, PAYMENT_METHOD_CHOICES, \
    PAYMENT_TYPE_CHOICES


class Workers(models.Model):
    name = models.CharField(verbose_name='Ф.И.О', max_length=300)
    phone = models.CharField(verbose_name='Номер телефона', max_length=40)
    work_price = models.IntegerField(verbose_name='Зарплата (сумма за 1 день)', null=True, blank=True)
    work_place = models.CharField(verbose_name='Место работы', max_length=40, null=True, blank=True)
    code = models.CharField(verbose_name='Код подтверждения', max_length=50, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name


class Car(models.Model):
    car_number = models.CharField(verbose_name='Номер машины:', max_length=20)
    driver = models.CharField(verbose_name='Водитель:', max_length=200)
    driver_phone = models.CharField(verbose_name='Контакты водителя:', max_length=400)

    def __str__(self):
        return self.car_number


class OutlayCategory(models.Model):
    name = models.CharField(max_length=255, verbose_name='Наименование категории расхода')
    type = models.CharField(max_length=255, verbose_name='Тип категории расхода',
                            choices=OUTLAY_TYPE_CHOICES, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория затрат'
        verbose_name_plural = 'Категории затрат'


class OutLay(models.Model):
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создание')
    outlay_type = models.ForeignKey('OutlayCategory',
                                    on_delete=models.PROTECT,
                                    verbose_name='Категории',
                                    null=True,
                                    blank=True)
    name = models.CharField(max_length=255, verbose_name='Причина')

    def __str__(self):
        return self.name


class PaymentLog(models.Model):
    """
        Таблица оплат
    """
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    amount = models.FloatField(default=0, verbose_name='Сумма')
    payment_type = models.CharField(max_length=10,
                                    verbose_name='Тип валюты',
                                    choices=PAYMENT_TYPE_CHOICES,
                                    default='cash')
    payment_method = models.CharField(max_length=10,
                                      verbose_name='Метод оплаты',
                                      choices=PAYMENT_METHOD_CHOICES,
                                      default='usd')
    outcat = models.IntegerField(default=0)
    outlay = models.IntegerField(default=0)
    outlay_child = models.IntegerField(default=0)
    user = models.ForeignKey(User,
                             on_delete=models.PROTECT,
                             verbose_name='Пользователь')
    comment = models.TextField(null=True,
                               blank=True)
    aor = models.BooleanField(default=False)
    amount_type = models.CharField(max_length=10,
                                   verbose_name='Тип валюты',
                                   choices=AMOUNT_TYPE_CHOICES)
    payment_log_type = models.CharField(max_length=255, verbose_name='Расход/Доход')
    rate = models.FloatField(default=0,
                             verbose_name='Курс доллара')


class Cashier(models.Model):
    amount = models.FloatField(default=0,
                               verbose_name='Сумма')
    payment_type = models.CharField(max_length=10,
                                    verbose_name='Тип валюты',
                                    choices=PAYMENT_TYPE_CHOICES,
                                    default='usd')

    def __str__(self):
        return self.payment_type


class SingletonModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super(SingletonModel, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class ProjectSetting(SingletonModel):
    rate = models.FloatField(default=0)

    def __str__(self):
        return str(self.rate)