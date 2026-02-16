from django.db.models import Sum

from income.models import IncomeItem, Income
from payment.models import ProjectSetting
from product.models import Product


def calculate_income_total(income_id):
    """
    :param income_id:
    :return:
    """
    total = IncomeItem.objects.filter(income=income_id) \
        .aggregate(Sum('total_uzs'), Sum('total_usd'))
    total_sum = total.get('total_uzs__sum')
    total_usd = total.get('total_usd__sum')
    if total:
        Income.objects.filter(pk=income_id).update(total_uzs=total_sum,
                                                   total_usd=total_usd,
                                                   rate=ProjectSetting.load().rate)
    else:
        Income.objects.filter(pk=income_id).update(total_uzs=0,
                                                   total_usd=0,
                                                   rate=ProjectSetting.load().rate)


def add_income_items_to_warehouse(income):
    income_items = IncomeItem.objects.filter(income=income)
    for wii in income_items:
        if wii.currency == 'uzs':
            self_price = (float(wii.price) / float(ProjectSetting.load().rate))
        else:
            self_price = wii.price
        obj, created = Product.objects.get_or_create(id=wii.product_id,
                                                     defaults={
                                                         'self_price': self_price,
                                                         'count': wii.count
                                                     })
        if not created:
            obj.self_price = calculate_self_price(self_price, wii.count, obj.price, obj.count)
            obj.count += wii.count
            obj.save()


def calculate_self_price(first_price, first_count, second_price, second_count):
    """
    :param first_price:
    :param first_count:
    :param second_price:
    :param second_count:
    :return:
    """
    if first_price < 0:
        first_price = second_price
    if second_price < 0:
        second_price = first_price
    first_total = (float(first_price) * float(first_count))
    second_total = (float(second_price) * float(second_count))

    return (float(first_total) + float(second_total)) / (float(first_count) + float(second_count))
