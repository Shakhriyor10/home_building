from datetime import datetime, timedelta

from django import template
import ast

# from past.types import basestring

register = template.Library()


# @register.filter('startswith')
# def startswith(text, starts):
#     if isinstance(text, basestring):
#         return text.startswith(starts)
#     return False


@register.filter(name='remove_zero')
def mul(val):
    try:
        return int(val)
    except ValueError:
        val = val.split(',')[0]
        val = val.split('.')[0]
        return val


@register.filter(name='add_hour')
def add_hour(val):
    try:
        date_now = datetime.now().replace(hour=int(val.split(':')[0]), minute=0, second=0, microsecond=0) + timedelta(
            hours=2)
        return date_now.time().strftime('%H:%M')
    except:
        return val


@register.filter(name='to_int')
def to_int(val):
    try:
        return int(val)
    except:
        return val


@register.filter(name='to_str')
def to_str(val):
    try:
        return str(val)
    except:
        return val


@register.filter(name='formater')
def formater(value):
    return str(value).replace('#', '')


@register.filter(name='get_tuple')
def get_tuple(value, index):
    helper = {
        'key': 0,
        'value': 1
    }
    return str(value).split("'")[1::2][helper[index]]


@register.filter(name='read_more')
def read_more(val):
    try:
        if len(val) > 15:
            return str(val[0:15] + '...')
        else:
            return str(val)
    except:
        return str(val)


@register.filter(name='total_amount_should_order')
def total_amount_should_order(payment_list):
    res = ast.literal_eval(payment_list)
    return res.items()


@register.filter(name='total_debt_student')
def total_debt_student(student_debt_list):
    res = ast.literal_eval(student_debt_list)
    d = {k: v for k, v in res.items() if v > 0}
    return d.items()


@register.filter(name='student_debt_exists_key')
def student_debt_exists_key(student_debt_list):
    res = ast.literal_eval(student_debt_list)
    d = {k: v for k, v in res.items() if v > 0}
    return d.keys()
