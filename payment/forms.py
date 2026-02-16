from django import forms

from payment.choices import EXPENSE_PAYMENT_TYPE_CHOICES, PAYMENT_METHOD_CHOICES
from payment.models import OutlayCategory, OutLay, Car, Workers


class WorkerCreateForm(forms.ModelForm):
    class Meta:
        model = Workers
        fields = ('name', 'phone', 'work_price', 'work_place', 'code',)


class OutlayCategoryForm(forms.ModelForm):
    class Meta:
        model = OutlayCategory
        fields = 'name', 'type'


class OutLayForm(forms.ModelForm):
    class Meta:
        model = OutLay
        fields = 'name',


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = '__all__'


class OutlayPaymentForm(forms.Form):
    outlay_category = forms.ModelChoiceField(label='Категория расхода', queryset=OutlayCategory.objects.all(),
                                             required=True)
    outlay_type = forms.ModelChoiceField(label='Причина', queryset=OutLay.objects.all(), required=True)
    worker = forms.ModelChoiceField(label='Сотрудник', queryset=Workers.objects.all(), required=True)
    car = forms.ModelChoiceField(label='Машина', queryset=Car.objects.all(), required=True)
    payment_amount = forms.FloatField(label='Сумма расхода')
    comment = forms.CharField(label='Комментарии', required=False)
    payment_type = forms.ChoiceField(label='Тип оплаты', choices=EXPENSE_PAYMENT_TYPE_CHOICES)
    payment_method = forms.ChoiceField(label='Метод оплаты', choices=PAYMENT_METHOD_CHOICES)


class ReportOutcomeForm(forms.Form):
    outlay_category = forms.ModelChoiceField(label='Категория расхода', queryset=OutlayCategory.objects.all(),
                                             required=True)
    worker = forms.ModelChoiceField(label='Сотрудник', queryset=Workers.objects.all(), required=False)
    car = forms.ModelChoiceField(label='Машина', queryset=Car.objects.all(), required=False)
