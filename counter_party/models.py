from django.db import models
from django.contrib.auth.models import User
from counter_party.choices import CONTR_AGENT_STATUS_CHOICES


class CounterParty(models.Model):
    name = models.CharField(max_length=255, verbose_name='Имя', unique=True)
    balance_usd = models.FloatField(default=0,
                                    verbose_name='USD')
    balance_uzs = models.FloatField(default=0,
                                    verbose_name='UZS')
    org_name = models.CharField(max_length=255, verbose_name='Название организации', null=True, blank=True)
    phone = models.CharField(max_length=255, verbose_name='Номер телефона', unique=True)
    phone2 = models.CharField(max_length=255, verbose_name='Дополнительный номер телефона', null=True, blank=True)
    address = models.CharField(max_length=255, verbose_name='Адресс', null=True, blank=True)
    inn = models.CharField(max_length=255, verbose_name='ИНН', null=True, blank=True)
    email = models.EmailField(verbose_name='E-mail', null=True, blank=True)
    status = models.IntegerField(choices=CONTR_AGENT_STATUS_CHOICES, verbose_name='Статус', default=0)
    sms_live = models.CharField(max_length=255, verbose_name='sms', null=True, blank=True)
    extra_info = models.TextField(verbose_name='Описание контр агента', null=True, blank=True)
    user = models.ForeignKey(User, verbose_name='Пользователь', blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        if not self.org_name:
            org_name = '-'
        else:
            org_name = self.org_name
        return f"{self.name} | {org_name} | {self.phone}"

    class Meta:
        verbose_name = 'Контр агент'
        verbose_name_plural = 'Контр агенты'
