from django.db import models
from django.contrib.auth.models import User
from warehouse.choices import WAREHOUSE_STATUS, WAREHOUSE_TYPE


class Warehouse(models.Model):
    title = models.CharField(max_length=255,
                             verbose_name='Название')
    status = models.CharField(max_length=255,
                              choices=WAREHOUSE_STATUS,
                              verbose_name='Статус',
                              default='active')

    def __str__(self):
        return self.title
