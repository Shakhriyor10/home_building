from django.contrib.auth.models import User

from payment.models import ProjectSetting, Cashier
from warehouse.forms import FirmBalanceConversionForm


def pages(request):
    first_tab = ProjectSetting.load()
    convert_form = FirmBalanceConversionForm
    data = {
        'ps': first_tab,
        'convert_form': convert_form,
        'cashiers': Cashier.objects.order_by('-payment_type')
    }
    return data
