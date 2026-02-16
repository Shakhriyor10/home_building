from django import forms

from payment.models import Cashier


class FirmBalanceConversionForm(forms.Form):
    cashiers = forms.ModelChoiceField(label='Конвертация с баланса:', required=True,
                                      queryset=Cashier.objects.all())
    cashiers_second = forms.ModelChoiceField(label='Конвертация на баланс:', required=True,
                                             queryset=Cashier.objects.all())
    amount = forms.FloatField(label='Сумма конвертации откуда', required=True)
    amount_second = forms.FloatField(label='Сумма конвертации куда', required=True)
    comment = forms.CharField(label='Комментарии', required=False)