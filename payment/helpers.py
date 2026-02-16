from django.db.models import F

from counter_party.models import CounterParty
from order.models import Order
from payment.models import Cashier, PaymentLog


def add_for_contr_agent_from_order(order, amount, payment_type):
    order_pk = Order.objects.get(pk=order.id)

    def usd():
        contr_agent = order_pk.counterparty
        contr_agent.balance_usd += float(amount)
        contr_agent.save()

    def uzs():
        contr_agent = order_pk.counterparty
        contr_agent.balance_uzs += float(amount)
        contr_agent.save()

    amount_type = {
        'usd': usd,
        'uzs': uzs,
    }
    return amount_type[payment_type]()


def add_balance_for_contr_agent(contr_agent, amount, payment_type):
    counterparty_pk = CounterParty.objects.get(pk=contr_agent.id)

    def usd(usd_contr_agent, usd_amount):
        usd_contr_agent.balance_usd += float(usd_amount)
        usd_contr_agent.save()

    def uzs(uzs_contr_agent, uzs_amount):
        uzs_contr_agent.balance_uzs += float(uzs_amount)
        uzs_contr_agent.save()

    amount_type = {
        'usd': usd,
        'uzs': uzs,
    }
    return amount_type[payment_type](counterparty_pk, amount)


def payment_income(amount, payment_type, payment_method, comment,
                   user, aor=False, outcat=0, outlay=0, **kwargs):
    """
    Create PaymentLog object for income cash payment
     1 -> outlay
     2 -> worker
     3 -> order
     4 -> counterparty
     5 -> student
     6, 7 - > conversion
     8 -> car
     9 -> worker
    :param amount:
    :param payment_type:
    :param payment_method:
    :param comment:
    :param user: -> user_id
    :param aor: -> Исключить из отчёта
    :param outcat:
    :param outlay:
    :return:
    """

    if outcat == 1:
        comment += " Оплата за приход №{}".format(outlay)
    elif outcat == 2:
        comment += " Оплата за заказ №{}".format(outlay)
    elif outcat == 3:
        comment += " Возврат расхода {}".format(kwargs['outlay_name'])
    elif outcat == 4:
        comment += " Пополнение баланса контрагента {}".format(kwargs['outlay_name'])
    elif outcat == 5:
        comment += " Оплата за доставку. Заказ №{}".format(outlay)
    elif outcat == 6:
        comment += " Возврат расхода на машину {}".format(kwargs['outlay_name'] + ' ' + kwargs['car_number'])
    elif outcat == 7:
        comment += " Возврат от зарплаты сотрудника {}".format(kwargs['outlay_name'] + ' ' + kwargs['worker'])
    elif outcat == 11:
        comment += " Возврат от зарплаты {}".format(kwargs['outlay_name'] + ', Станок: ' + kwargs['machine'])
    elif outcat == 12:
        comment += " Оплата за производственное заказ №{}".format(outlay)

    if payment_method == 'cash' and float(amount) > 0 and outcat != 11:
        Cashier.objects.filter(payment_type=payment_type).update(amount=F('amount') + float(amount))
    elif payment_method == 'enumeration' and float(amount) > 0 and outcat != 11:
        Cashier.objects.filter(payment_type='bank').update(amount=F('amount') + float(amount))

    payment = PaymentLog.objects.create(
        amount=amount,
        payment_type=payment_type,
        payment_method=payment_method,
        outcat=outcat,
        outlay=outlay,
        outlay_child=kwargs.get('outlay_child', 0),
        comment=comment,
        user=user,
        aor=aor,
        payment_log_type='income'
    )

    return dict(
        {'pk': payment.pk,
         'created': payment.created.strftime('%d-%m-%Y | %H:%M'),
         'payment_method': payment.payment_method,
         'payment_type': payment.payment_type,
         'amount': payment.amount,
         'comment': payment.comment})


def remove_balance_for_contr_agent(contr_agent, amount, payment_type):
    counterparty_pk = CounterParty.objects.get(pk=contr_agent.id)

    def usd(usd_contr_agent, usd_amount):
        usd_contr_agent.balance_usd -= float(usd_amount)
        usd_contr_agent.save()

    def uzs(uzs_contr_agent, uzs_amount):
        uzs_contr_agent.balance_uzs -= float(uzs_amount)
        uzs_contr_agent.save()

    amount_type = {
        'usd': usd,
        'uzs': uzs,
    }
    return amount_type[payment_type](counterparty_pk, amount)


def payment_outcome(amount, payment_type, payment_method, comment,
                    user, aor=False, outcat=0, outlay=0, **kwargs):
    """
    Create PaymentLog object for income cash payment
     1 -> outlay
     2 -> salary_worker
     3 -> order
     4 -> counterparty
     5- > student
     8 -> car
     9 -> worker
    :param amount:
    :param payment_type:
    :param payment_method:
    :param comment:
    :param user: -> user_id
    :param aor: -> Исключить из отчёта
    :param outcat:
    :param outlay:
    :return:
    """
    if outcat == 1:
        comment += " Расход за приход №{}".format(outlay)
    elif outcat == 2:
        comment += " Расход за заказ №{}".format(outlay)
    elif outcat == 3:
        comment += " Расход за {}".format(kwargs['outlay_name'])
    elif outcat == 4:
        comment += " Выдача денег контрагенту {}".format(kwargs['outlay_name'])
    elif outcat == 5:
        comment += " (Расход) за доставку №{}".format(outlay)
    elif outcat == 6:
        comment += " Расход на машину {}".format(kwargs['outlay_name'] + ' ' + kwargs['car_number'])
    elif outcat == 7:
        comment += " Зарплата сотрудника {}".format(kwargs['outlay_name'] + ' ' + kwargs['worker'])
    elif outcat == 8:
        comment += " Расод за возврат товара {}".format(kwargs['product_name'] + ' ' + kwargs['count'] + 'x')
    elif outcat == 9 and outcat == 10:
        comment += " Конвертация баланса аегнта {}".format(kwargs['agent_name'] + ' с Курсом: ' + kwargs['rate'])
    elif outcat == 11:
        comment += " Расход на {}".format(kwargs['outlay_name'] + ', Станок: ' + kwargs['machine'])
    elif outcat == 12:
        comment += " Расход за производственное заказ №{}".format(outlay)

    if payment_method == 'cash' and float(amount) > 0 and outcat < 9:
        Cashier.objects.filter(payment_type=payment_type).update(amount=F('amount') - float(amount))
    elif payment_method == 'enumeration' and float(amount) > 0:
        Cashier.objects.filter(payment_type='bank').update(amount=F('amount') - float(amount))

    payment = PaymentLog.objects.create(
        amount=amount,
        payment_type=payment_type,
        payment_method=payment_method,
        outcat=outcat,
        outlay=outlay,
        outlay_child=kwargs.get('outlay_child', 0),
        comment=comment,
        user=user,
        aor=aor,
        payment_log_type='outcome'
    )

    return dict(
        {'pk': payment.pk,
         'created': payment.created.strftime('%d-%m-%Y | %H:%M'),
         'payment_method': payment.payment_method,
         'payment_type': payment.payment_type,
         'amount': payment.amount,
         'comment': payment.comment})
