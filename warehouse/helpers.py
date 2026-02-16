from django.db.models import F
from django.urls import reverse

from payment.helpers import payment_income
from payment.models import ProjectSetting, Cashier


def change_rate(post_request, user_request):
    new_rate = post_request.get('rate', 0)
    ProjectSetting.objects.update(rate=new_rate)
    return dict(
        {'rate': new_rate})


def conversion_balance(post_request, user_request):
    cashiers = post_request.get('cashiers', '')
    cashiers_second = post_request.get('cashiers_second', '')
    amount = post_request.get('amount', '')
    amount_second = post_request.get('amount_second', '')
    comment = post_request.get('comment', '')
    cashier = Cashier.objects.get(pk=cashiers)
    cashier_second = Cashier.objects.get(pk=cashiers_second)
    if cashiers and cashiers_second:
        Cashier.objects.filter(pk=cashiers).update(amount=F('amount') - float(amount))
        Cashier.objects.filter(pk=cashiers_second).update(amount=F('amount') + float(amount_second))
        if cashier_second.payment_type == 'uzs' or cashier_second.payment_type == 'bank':
            payment_type = 'uzs'
        else:
            payment_type = 'usd'
        print(payment_type)
        payment_income(amount_second, payment_type, 'cash', comment, user_request, False, 11, cashier.pk,
                       income_amount=amount_second, outlay_child=cashier_second.pk,
                       cash_first=cashier.get_payment_type_display(),
                       cash_second=cashier_second.get_payment_type_display())
    return dict({'back_url': reverse(post_request.get('back_url', 'home')),
                 'cashier_type_first': cashier.payment_type,
                 'cashier_type_second': cashier_second.payment_type,
                 'amount_first': amount,
                 'amount_second': amount_second})
