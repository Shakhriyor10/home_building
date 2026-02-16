from django.db.models import Sum, Q, F, Subquery, OuterRef
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, ListView, UpdateView, TemplateView
from django.views.generic.base import View

from counter_party.models import CounterParty
from order.helpers import calculate_order_total, contr_agent_balance_outcome, contr_agent_balance_income
from order.models import Order, OrderReturnItem, OrderItem
from payment.helpers import payment_income
from payment.models import ProjectSetting, PaymentLog
from product.models import Product


class OrderList(ListView):
    template_name = 'order_list.html'
    model = Order
    context_object_name = 'orders'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(OrderList, self).get_context_data(**kwargs)
        startdate = self.request.GET.get('startdate', None)
        enddate = self.request.GET.get('enddate', None)
        context['startdate'] = startdate
        context['enddate'] = enddate
        return context

    def get_queryset(self):
        startdate = self.request.GET.get('startdate', None)
        enddate = self.request.GET.get('enddate', None)
        if startdate and enddate:
            return Order.objects.filter(created__range=[startdate + " 00:00", enddate + " 23:59"]) \
                .select_related('user').order_by('-created')
        else:
            return Order.objects.order_by('-id')


class OrderCreate(CreateView):
    template_name = 'order_create.html'
    model = Order
    fields = ['counter_party']
    success_url = '/order/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.rate = ProjectSetting.load().rate
        return super(OrderCreate, self).form_valid(form)


class OrderUpdate(UpdateView):
    template_name = 'order_update.html'
    model = Order
    fields = '__all__'
    success_url = '/order/'


class OrderDetailView(TemplateView):
    template_name = 'OrderDetail.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(OrderDetailView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, pk, **kwargs):
        context = super(OrderDetailView, self).get_context_data(**kwargs)
        payments = PaymentLog.objects.filter(outlay=pk, outcat__in=[2, 5])
        order = Order.objects.prefetch_related('orderitem_set') \
            .select_related('user', 'counter_party') \
            .get(id=pk)
        order_item_total = order.orderitem_set.all().aggregate(Sum('total_uzs'), Sum('total_usd'))
        context['order'] = order
        context['order_items'] = OrderItem.objects.select_related('product') \
            .filter(order_id=pk)
        context['order_return_items'] = OrderReturnItem.objects.select_related('order_item__product',
                                                                               'order_item') \
            .filter(order_item__order_id=pk)
        context['order_items_total'] = order_item_total
        context['products'] = Product.objects.filter(count__gt=0)
        warehouse_count_total = 0
        context['warehouse_count'] = warehouse_count_total
        context['payments'] = payments
        total_uzs = 0
        total_usd = 0
        for payment in payments:
            if payment.payment_type == 'usd':
                total_usd += payment.amount
            else:
                total_uzs += payment.amount
        context['total_uzs'] = total_uzs
        context['total_usd'] = total_usd
        return context

    def post(self, request, pk, **kwargs):
        products = request.POST.getlist('products', None)
        if products:
            for product_id in products:
                print(request.POST)
                count = request.POST.get('count_{}'.format(product_id), 0)
                price = request.POST.get('price_{}'.format(product_id), 0)
                is_currency = request.POST.get('is_currency_{}'.format(product_id), None)
                total_price = float(price) * float(count)
                if is_currency:
                    data = {
                        'count': count,
                        'price': price,
                        'total_usd': total_price,
                        'rate': ProjectSetting.load().rate
                    }
                else:
                    data = {
                        'count': count,
                        'price': price,
                        'total_uzs': total_price,
                        'rate': ProjectSetting.load().rate
                    }
                product = Product.objects.get(id=product_id)
                obj, created = OrderItem.objects.get_or_create(
                    order_id=pk,
                    product=product,
                    defaults=data
                )
                if not created:
                    obj.count = count
                    obj.price = price
                    obj.rate = ProjectSetting.load().rate
                    if is_currency:
                        obj.total_usd = float(count) * float(price)
                        obj.total_uzs = 0
                    else:
                        obj.total_usd = 0
                        obj.total_uzs = float(count) * float(price)
                    obj.save()
        calculate_order_total(pk)
        return redirect(reverse('order_detail', kwargs={'pk': pk}))


class OrderActionView(View):
    def post(self, request, pk):
        action = request.POST.get('action', '')
        data = request.POST.get('data', '')
        if action == 'close_order':
            order = Order.objects.get(pk=pk)
            order.status = 3
            order.rate = ProjectSetting.load().rate
            order.save()
            if order.total_uzs > 0:
                contr_agent_balance_outcome(order.counter_party_id, 'uzs', order.total_uzs)

            if order.total_usd > 0:
                contr_agent_balance_outcome(order.counter_party_id, 'usd', order.total_usd)
            order_item_sub = OrderItem.objects \
                .filter(order=order, product_id=OuterRef('pk')) \
                .values('product_id') \
                .annotate(total_count=Sum('count')) \
                .values('total_count')
            Product.objects.prefetch_related('order_item').filter(order_item__order=order) \
                .annotate(saled_count=Subquery(order_item_sub.values('total_count')[:1])) \
                .update(count=F('count') - F('saled_count'))
        elif action == 'delete_order_item':
            OrderItem.objects.filter(pk=data).delete()
            calculate_order_total(pk)
        elif action == 'move_to_trash':
            order = Order.objects.get(pk=pk)
            order.status = 4
            order.save()
        elif action == 'order_return_item':
            returned_item = self.request.POST.get('order_return_item_id', 0)
            count = self.request.POST.get('order_change_item_count', 0)
            order_return_item = OrderReturnItem.objects.create(count=count,
                                                               order_item_id=returned_item,
                                                               rate=ProjectSetting.load().rate)
            if order_return_item.order_item.total_usd == 0:
                order_return_item.total_uzs = float(order_return_item.order_item.price) \
                                              * float(order_return_item.count)
                contr_agent_balance_income(order_return_item.order_item.order.counter_party.id, 'uzs',
                                           order_return_item.total_uzs)
            if order_return_item.order_item.total_uzs == 0:
                order_return_item.total_usd = float(order_return_item.order_item.price) \
                                              * float(order_return_item.count)
                contr_agent_balance_income(order_return_item.order_item.order.counter_party.id, 'usd',
                                           order_return_item.total_usd)
            order_return_item.save()
            wp = Product.objects.get(pk=order_return_item.order_item.product.id)
            wp.count += float(count)
            wp.save()
            calculate_order_total(pk)
        elif action == 'pay_order':
            order = Order.objects.get(pk=pk)
            amount = request.POST.get('amount', 0)
            payment_type = request.POST.get('payment_type', 'usd')
            payment_method = request.POST.get('payment_method', '')
            comment = request.POST.get('comment', '')
            for_deliver = request.POST.get('for_deliver', '')
            if for_deliver:
                print(for_deliver, 'for_deliver')
                payment_income(amount, payment_type, payment_method, comment, request.user, False, outcat=5,
                               outlay=order.pk)
            else:
                contr_agent_balance_income(order.counter_party_id, payment_type, amount)
                payment_income(amount, payment_type, payment_method, comment, request.user,
                               False, outcat=2, outlay=order.pk)
        return redirect(reverse('order_detail', kwargs={'pk': pk}))
