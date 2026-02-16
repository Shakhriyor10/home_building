from datetime import datetime

from django.db.models import Sum
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import ListView, CreateView, TemplateView
from django.views.generic.base import View

from income.helpers import add_income_items_to_warehouse, calculate_income_total
from income.models import Income, IncomeItem
from order.helpers import contr_agent_balance_income, contr_agent_balance_outcome
from payment.choices import PAYMENT_TYPE_CHOICES, PAYMENT_METHOD_CHOICES
from payment.helpers import payment_outcome
from payment.models import ProjectSetting, PaymentLog
from product.models import Product


class IncomeListView(ListView):
    template_name = 'Income.html'
    model = Income
    context_object_name = 'incomes'
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(IncomeListView, self).get_context_data(**kwargs)
        context['selected_status'] = self.request.GET.get('status', '')
        return context

    def get_queryset(self):
        status = self.request.GET.get('status', '')
        if status == '' or not status:
            return Income.objects.filter(status__lt=3).order_by('-created')
        elif status == '3':
            return Income.objects.filter(status=3).order_by('-created')
        else:
            return Income.objects.filter(status=status).order_by('-created')


class IncomeCreateView(CreateView):
    template_name = 'IncomeAdd.html'
    model = Income
    fields = ['counter_party']

    def get_context_data(self, **kwargs):
        context = super(IncomeCreateView, self).get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.created = datetime.now()
        form.instance.rate = ProjectSetting.load().rate
        return super(IncomeCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('income_detail', kwargs={'pk': self.object.pk})


class IncomeDetailView(TemplateView):
    template_name = 'IncomeDetail.html'

    def get_context_data(self, pk, **kwargs):
        context = super(IncomeDetailView, self).get_context_data(**kwargs)
        income = Income.objects.get(pk=pk)
        context['income'] = Income.objects.select_related('user', 'counter_party').get(pk=pk)
        context['income_item'] = IncomeItem.objects.select_related('product', 'income__counter_party') \
            .filter(income_id=pk)
        context['payment_types'] = dict(PAYMENT_TYPE_CHOICES)
        context['payment_methods'] = dict(PAYMENT_METHOD_CHOICES)
        context['products'] = Product.objects.all()
        if context['income'].status == 1:
            context['payments'] = PaymentLog.objects.filter(outcat=1, outlay=pk)
            context['payment_total'] = PaymentLog.objects.filter(outcat=1, outlay=pk).aggregate(Sum('amount'))[
                'amount__sum']
        return context

    def post(self, request, pk, **kwargs):
        products = request.POST.getlist('products', None)
        if products:
            for product_id in products:
                print(request.POST)
                count = request.POST.get('count_{}'.format(product_id), 0)
                price = request.POST.get('price_{}'.format(product_id), 0)
                currency = request.POST.get('on_USD_{}'.format(product_id), None)
                product = Product.objects.get(pk=product_id)
                total = 0
                total = float(count) * float(price)
                if currency:
                    data = {
                        'count': count,
                        'price': price,
                        'total_usd': total,
                        'currency': 'usd'
                    }
                else:
                    data = {
                        'count': count,
                        'price': price,
                        'total_uzs': total,
                        'currency': 'uzs'
                    }
                obj, created = IncomeItem.objects.get_or_create(
                    income_id=pk,
                    product=product,
                    defaults=data
                )
                if not created:
                    obj.currency = currency
                    obj.count = count
                    obj.price = price
                    total = float(count) * float(price)
                    if currency:
                        obj.total_usd = total
                    else:
                        obj.total_uzs = total
                    obj.rate = ProjectSetting.load().rate
                    obj.save()

        calculate_income_total(pk)
        # calculate_product_count(pk, item.product)

        return redirect(reverse('income_detail', kwargs={'pk': pk}))


class IncomeActionView(View):
    def post(self, request, pk):
        action = request.POST.get('action', '')
        data = request.POST.get('data', '')
        income_items = IncomeItem.objects.filter(income_id=pk)
        warehouse_income = Income.objects.get(pk=pk)
        if action == 'change_rate':
            new_rate = request.POST.get('rate', 0)
            ProjectSetting.rate = new_rate
        if action == 'close_income':
            # income_doc(pk)
            warehouse_income.status = 1
            warehouse_income.save()
            add_income_items_to_warehouse(warehouse_income)
            if warehouse_income.total_usd > 0:
                contr_agent_balance_income(warehouse_income.counter_party_id, 'usd', warehouse_income.total_usd)
            if warehouse_income.total_uzs > 0:
                contr_agent_balance_income(warehouse_income.counter_party_id, 'uzs', warehouse_income.total_uzs)

            return redirect(reverse('income_detail', kwargs={'pk': pk}))
        if action == 'completed_income':
            warehouse_income.status = 2
            warehouse_income.save()
            return redirect(reverse('income_detail', kwargs={'pk': pk}))
        elif action == 'delete_income_item':
            print(data)
            IncomeItem.objects.get(pk=data).delete()
            calculate_income_total(pk)
            return redirect(reverse('income_list'))
        elif action == 'stop_income':
            Income.objects.filter(pk=pk).update(status=0)
            for income_item in income_items:
                print(income_item.product.id)
                wp = Product.objects.get(product_id=income_item.product.id)
                wp.count -= income_item.count
                wp.save()
            return redirect(reverse('income_list'))
        elif action == 'delete_income':
            Income.objects.filter(pk=pk).update(status=3)
            contr_agent_balance_income(warehouse_income.counter_party.id, 'usd', warehouse_income.total_usd)
            contr_agent_balance_income(warehouse_income.counter_party.id, 'uzs', warehouse_income.total_uzs)
            for income_item in income_items:
                wp = Product.objects.get(product_id=income_item.product.id)
                wp.count -= income_item.count
                wp.save()
            return redirect(reverse('income_detail', kwargs={'pk': pk}))
        elif action == 'income_payment':
            print(action)
            amount = request.POST.get('amount', '')
            payment_type = request.POST.get('payment_type', '')
            payment_method = request.POST.get('payment_method', '')
            comment = request.POST.get('comment', '')
            contr_agent_balance_outcome(warehouse_income.counter_party_id, payment_type, amount)
            payment_outcome(amount, payment_type, payment_method, comment, request.user, False, outcat=1,
                            outlay=warehouse_income.pk)
            return redirect(reverse('income_detail', kwargs={'pk': pk}))

