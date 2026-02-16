from django.db import models

from product.choices import PRODUCT_PRODUCT_STATUS


class Product(models.Model):
    title = models.CharField(verbose_name='Название',
                             max_length=255)
    size = models.CharField(verbose_name='Размер(ШхВхТ)', blank=True, null=True,
                            max_length=255)
    price = models.FloatField(verbose_name='Цена',
                              default=0)
    code = models.CharField(verbose_name='Код продукта',
                            max_length=255,
                            null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    count = models.FloatField(verbose_name='Количество (кг)', default=0)
    status = models.CharField(max_length=255,
                              choices=PRODUCT_PRODUCT_STATUS,
                              verbose_name='Статус',
                              null=True,
                              blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'