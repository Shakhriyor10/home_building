from django.db.models import Subquery, OuterRef, F, Sum

from counter_party.models import CounterParty
from order.models import OrderItem, OrderReturnItem, Order
from product.models import Product


def calculate_order_total(order_id):
    """
    :param order_id:
    :return:
    """

    OrderItem.objects.select_related('product') \
        .filter(order_id=order_id, total_usd__gt=0) \
        .update(total_usd=F('count') * F('price'))
    OrderItem.objects.select_related('product') \
        .filter(order_id=order_id, total_uzs__gt=0) \
        .update(total_uzs=F('count') * F('price'))
    order_items_total = OrderItem.objects. \
        filter(order_id=order_id, status=0). \
        aggregate(Sum('total_uzs'), Sum('total_usd'))
    order_return_total = OrderReturnItem.objects \
        .filter(order_item__order_id=order_id) \
        .aggregate(Sum('total_uzs'), Sum('total_usd'))
    if order_items_total.get('total_uzs__sum'):
        total_sum = order_items_total.get('total_uzs__sum', 0)
    else:
        total_sum = 0

    if order_items_total.get('total_usd__sum'):
        total_usd = order_items_total.get('total_usd__sum')
    else:
        total_usd = 0
    if order_return_total.get('total_uzs__sum', 0):
        total_sum -= float(order_return_total.get('total_uzs__sum', 0))
    if order_return_total.get('total_usd__sum', 0):
        total_usd -= float(order_return_total.get('total_usd__sum', 0))
    if order_items_total:
        Order.objects.filter(pk=order_id) \
            .update(total_uzs=total_sum, total_usd=total_usd)
    else:
        Order.objects.filter(pk=order_id).update(total_uzs=0, total_usd=0)


def contr_agent_balance_income(contr_agent_id, payment_type, amount):
    """
    Плюсуем баланс контрагента
    :param contr_agent_id:
    :param payment_type:
    :param amount:
    :return:
    """
    if payment_type == 'usd':
        CounterParty.objects.filter(id=contr_agent_id) \
            .update(balance_usd=F('balance_usd') + int(amount))
    else:
        CounterParty.objects.filter(id=contr_agent_id) \
            .update(balance_uzs=F('balance_uzs') + int(amount))


def contr_agent_balance_outcome(contr_agent_id, payment_type, amount):
    """
    Минусем баланс контрагента
    :param contr_agent_id:
    :param payment_type:
    :param amount:
    :return:
    """
    if payment_type == 'usd':
        CounterParty.objects.filter(id=contr_agent_id) \
            .update(balance_usd=F('balance_usd') - int(amount))
    else:
        CounterParty.objects.filter(id=contr_agent_id) \
            .update(balance_uzs=F('balance_uzs') - int(amount))


def product_to_reserve_from_order(order):
    """
    Sending products to reserve after order closed
    :param order:
    :return:
    """