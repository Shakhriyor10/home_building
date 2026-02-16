from datetime import datetime

from django.db.models import Sum, Q, OuterRef
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView, ListView, CreateView, UpdateView
from sql_util.aggregates import SubqueryAggregate

from income.helpers import calculate_income_total, add_income_items_to_warehouse
from income.models import Income, IncomeItem
from order.helpers import contr_agent_balance_income, contr_agent_balance_outcome
from payment.choices import PAYMENT_TYPE_CHOICES, PAYMENT_METHOD_CHOICES
from payment.helpers import payment_outcome
from payment.models import ProjectSetting, PaymentLog
from product.models import Product


class ProductView(ListView):
    template_name = 'product_list.html'
    model = Product
    context_object_name = 'products'
    queryset = Product.objects.order_by('-id')


class ProductCreate(CreateView):
    template_name = 'product_create.html'
    model = Product
    fields = ['title', 'price', 'status', 'code']
    success_url = '/'


class ProductUpdate(UpdateView):
    template_name = 'product_udate.html'
    model = Product
    fields = ['title', 'price', 'status', 'code']
    success_url = '/'


class ProductReport(TemplateView):
    template_name = 'product_report.html'

    def get_context_data(self, **kwargs):
        start_date = self.request.GET.get('start_date', '')
        end_date = self.request.GET.get('end_date', '')
        context = super(ProductReport, self).get_context_data(**kwargs)
        context['selected_start_date'] = start_date
        context['selected_end_date'] = end_date

        if not start_date and not end_date:
            start_date = datetime.now().strftime('%Y-%m-%d') + " 00:00"
            end_date = datetime.now().strftime('%Y-%m-%d') + " 23:59"
        else:
            start_date = start_date + " 00:00"
            end_date = end_date + " 23:59"
        products = Product.objects.all()
        products = products.annotate(
            product_income_total=SubqueryAggregate('incomeitem__count',
                                                   filter=Q(product_id=OuterRef('id'),
                                                            income__status=2,
                                                            income__created__range=[start_date,
                                                                            end_date]),
                                                   aggregate=Sum),
            product_order_total=SubqueryAggregate('order_item__count',
                                                  filter=Q(product_id=OuterRef('id'),
                                                           order__status=3,
                                                           order__created__range=[start_date,
                                                                                  end_date]),
                                                  aggregate=Sum),
            product_return_item_total=SubqueryAggregate('order_item__orderreturnitem__count',
                                                        filter=Q(order_item__product_id=OuterRef('id'),
                                                                 order_item__order__created__range=[start_date,
                                                                                                    end_date]),
                                                        aggregate=Sum)
        )
        products_list = list(products.filter(product_income_total__gt=0).values_list('id', flat=True)) \
                        + list(products.filter(product_order_total__gt=0).values_list('id', flat=True)) \
                        + list(products.filter(product_return_item_total__gt=0).values_list('id', flat=True))
        context['products'] = products.filter(id__in=products_list)
        return context
