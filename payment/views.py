from django.db.models import Sum, Subquery, OuterRef
from datetime import datetime
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView, CreateView, UpdateView, DetailView, TemplateView

from counter_party.models import CounterParty
from payment.forms import OutlayCategoryForm, OutLayForm, OutlayPaymentForm, CarForm, ReportOutcomeForm, \
    WorkerCreateForm
from payment.helpers import payment_outcome, payment_income
from payment.models import Workers, Car, OutlayCategory, OutLay, PaymentLog


class WorkerList(ListView):
    template_name = 'workers_list.html'
    model = Workers
    context_object_name = 'worker'
    queryset = Workers.objects.order_by('-id')


class WorkerCreate(TemplateView):
    template_name = 'worket_create.html'
    model = Workers

    # def get_context_data(self, **kwargs):
    #     context = super(WorkerCreate, self).get_context_data(**kwargs)
    #     context['forms'] = WorkerCreateForm()
    #     return context

    def post(self, request):
        name = self.request.POST.get('name', None)
        phone = self.request.POST.get('phone', None)
        work_price = self.request.POST.get('work_price', None)
        work_place = self.request.POST.get('work_place', None)
        code = self.request.POST.get('code', None)
        user = self.request.user
        Workers.objects.create(name=name,
                               phone=phone,
                               work_price=work_price,
                               work_place=work_place,
                               code=code,
                               user=user)
        return redirect(reverse('workers'))


class WorkerUpdate(UpdateView):
    template_name = 'worker_update.html'
    model = Workers
    fields = '__all__'
    success_url = '/workers/'


class CarList(ListView):
    template_name = 'car_list.html'
    model = Car
    context_object_name = 'cars'
    queryset = Car.objects.order_by('-id')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CarList, self).get_context_data(**kwargs)
        context['forms'] = CarForm()
        return context

    def post(self, request):
        form = CarForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect(reverse('cars'))


class CarUpdate(UpdateView):
    template_name = 'car_update.html'
    model = Car
    fields = '__all__'
    success_url = '/cars/'


class OutlayCategoryList(ListView):
    template_name = 'outlay_category_list.html'
    model = OutlayCategory
    context_object_name = 'outlay_category'
    queryset = OutlayCategory.objects.order_by('-id')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(OutlayCategoryList, self).get_context_data(**kwargs)
        context['forms'] = OutlayCategoryForm()
        return context

    def post(self, request):
        form = OutlayCategoryForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect(reverse('outlay_cat'))


class OutlayCategoryDetail(ListView):
    template_name = 'outlay_category_detail.html'
    model = OutLay
    context_object_name = 'outlay'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(OutlayCategoryDetail, self).get_context_data(**kwargs)
        outlay_cat = OutlayCategory.objects.get(pk=self.kwargs['pk'])
        context['name_cat'] = outlay_cat
        context['outlay'] = OutLay.objects.filter(outlay_type=outlay_cat.pk)
        context['forms'] = OutLayForm()
        return context

    def post(self, request, pk):
        name = self.request.POST.get('name', None)
        outlay_type = OutlayCategory.objects.get(id=pk)
        OutLay.objects.create(outlay_type=outlay_type,
                              name=name)
        return redirect(reverse('outlay_cat_detail', kwargs={'pk': pk}))


class OutlayPaymentCreateView(TemplateView):
    template_name = 'outlay.html'

    def get_context_data(self, **kwargs):
        context = super(OutlayPaymentCreateView, self).get_context_data(**kwargs)
        context['outlay_payment_form'] = OutlayPaymentForm
        context['outlay_categories'] = OutlayCategory.objects.all()
        context['outlay_type'] = OutLay.objects.select_related('outlay_type').all()
        context['payment_logs'] = PaymentLog.objects.filter(payment_log_type='outcome').order_by('-created')
        return context

    def post(self, request, **kwargs):
        value_outlay_category = self.request.POST.get('outlay_category', '')
        value_outlay_type = self.request.POST.get('outlay_type', '')
        value_outlay_worker = self.request.POST.get('worker', None)
        value_outlay_car = self.request.POST.get('car', None)
        value_outlay_comment = self.request.POST.get('comment', '')
        value_outlay_amount = self.request.POST.get('payment_amount', '')
        value_outlay_amount_type = self.request.POST.get('payment_type', '')
        value_outlay_amount_method = self.request.POST.get('payment_method', '')

        outlay_category = OutlayCategory.objects.get(pk=value_outlay_category)
        outlay = OutLay.objects.get(pk=value_outlay_type)

        if outlay_category.type == 'worker':
            worker = Workers.objects.get(pk=value_outlay_worker)
            payment_outcome(value_outlay_amount, value_outlay_amount_type, value_outlay_amount_method,
                            value_outlay_comment,
                            self.request.user, True, 2, value_outlay_type,
                            outlay_name=outlay.outlay_type.name, worker=worker.user,
                            outlay_child=value_outlay_worker)
        elif outlay_category.type == 'car':
            car = Car.objects.get(pk=value_outlay_car)
            payment_outcome(value_outlay_amount, value_outlay_amount_type, value_outlay_amount_method,
                            value_outlay_comment,
                            self.request.user, True, 8, value_outlay_type,
                            outlay_name=outlay.name, car_number=car.car_number, outlay_child=car.id)
        else:
            payment_outcome(value_outlay_amount, value_outlay_amount_type, value_outlay_amount_method,
                            value_outlay_comment,
                            self.request.user, True, 1, value_outlay_type,
                            outlay_name=outlay.outlay_type.name)
        return redirect(reverse('outlay'))


class OutlayPaymentReturnCreateView(TemplateView):
    template_name = 'return_outlay_create.html'

    def get_context_data(self, **kwargs):
        context = super(OutlayPaymentReturnCreateView, self).get_context_data(**kwargs)
        context['outlay_payment_form'] = OutlayPaymentForm
        context['outlay_categories'] = OutlayCategory.objects.all()
        context['outlay_type'] = OutLay.objects.select_related('outlay_type').all()
        context['payment_logs'] = PaymentLog.objects.filter(payment_log_type='income').order_by('-created')
        return context

    def post(self, request, **kwargs):
        value_outlay_category = self.request.POST.get('outlay_category', '')
        value_outlay_type = self.request.POST.get('outlay_type', '')
        value_outlay_worker = self.request.POST.get('worker', None)
        value_outlay_car = self.request.POST.get('car', None)
        value_outlay_comment = self.request.POST.get('comment', '')
        value_outlay_amount = self.request.POST.get('payment_amount', '')
        value_outlay_amount_type = self.request.POST.get('payment_type', '')
        value_outlay_amount_method = self.request.POST.get('payment_method', '')

        outlay_category = OutlayCategory.objects.get(pk=value_outlay_category)
        outlay = OutLay.objects.get(pk=int(value_outlay_type))
        if outlay_category.type == 'worker':
            worker = Workers.objects.get(pk=value_outlay_worker)
            payment_income(value_outlay_amount, value_outlay_amount_type, value_outlay_amount_method,
                           value_outlay_comment,
                           self.request.user, True, 2, value_outlay_type,
                           outlay_name=outlay.outlay_type.name, worker=worker.user,
                           outlay_child=value_outlay_worker)
        elif outlay_category.type == 'car':
            car = Car.objects.get(pk=value_outlay_car)
            payment_income(value_outlay_amount, value_outlay_amount_type, value_outlay_amount_method,
                           value_outlay_comment,
                           self.request.user, True, 8, value_outlay_type,
                           outlay_name=outlay.name, car_number=car.car_number, outlay_child=car.id)
        else:
            payment_income(value_outlay_amount, value_outlay_amount_type, value_outlay_amount_method,
                           value_outlay_comment,
                           self.request.user, True, 1, value_outlay_type,
                           outlay_name=outlay.outlay_type.name)
        return redirect(reverse('return_outlay'))


class ReportsIncomePaymentsView(ListView):
    template_name = 'report_income_payment.html'
    model = PaymentLog
    context_object_name = 'report_income_payments'
    paginate_by = 20

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ReportsIncomePaymentsView, self).get_context_data(**kwargs)
        counterparty = self.request.GET.get('counterparty', '')
        startdate = self.request.GET.get('startdate', None)
        enddate = self.request.GET.get('enddate', None)
        context['counterparties'] = CounterParty.objects.all()
        context['startdate'] = startdate
        context['enddate'] = enddate
        context['selected_counterparty'] = counterparty
        if startdate and enddate:
            payments = PaymentLog.objects.filter(created__range=[startdate + " 00:00", enddate + " 23:59"],
                                                 payment_log_type='income').select_related('user').order_by('-created')
            if counterparty and counterparty != 'all':
                payments = payments.filter(outcat=4, outlay=counterparty)
            context['dollar_amount'] = payments.filter(payment_type='usd').select_related('user') \
                .aggregate(Sum('amount'))
            context['sum_amount'] = payments.filter(payment_type='uzs').select_related('user') \
                .aggregate(Sum('amount'))
        else:
            if counterparty and counterparty != 'all':
                payments = PaymentLog.objects.filter(outcat=4, outlay=counterparty, payment_log_type='income') \
                    .select_related('user').order_by('-created')
                context['dollar_amount'] = payments.filter(payment_type='usd').aggregate(Sum('amount'))
                context['sum_amount'] = payments.filter(payment_type='uzs').aggregate(Sum('amount'))
            else:
                date_now = datetime.today().date()
                context['dollar_amount'] = PaymentLog.objects.filter(
                    created__range=[str(date_now) + " 00:00", str(date_now) + " 23:59"],
                    payment_type='usd', payment_log_type='income') \
                    .order_by('-created').select_related('user').aggregate(Sum('amount'))
                context['sum_amount'] = PaymentLog.objects.filter(
                    created__range=[str(date_now) + " 00:00", str(date_now) + " 23:59"],
                    payment_type='uzs', payment_log_type='income') \
                    .order_by('-created').select_related('user').aggregate(Sum('amount'))
        return context

    def get_queryset(self):
        startdate = self.request.GET.get('startdate', '')
        enddate = self.request.GET.get('enddate', '')
        counterparty = self.request.GET.get('counterparty', '')
        if counterparty and counterparty != 'all':
            outlay_ids = CounterParty.objects.filter(pk=counterparty).values_list('id', flat=True)
        if startdate and enddate:
            if counterparty and counterparty != 'all':
                return PaymentLog.objects.filter(created__range=[startdate + " 00:00", enddate + " 23:59"],
                                                 payment_log_type='income',
                                                 outcat=4,
                                                 outlay__in=outlay_ids) \
                    .annotate(counterparty_payment=Subquery(CounterParty.objects.filter(id=OuterRef('outlay'))
                                                            .select_related('user')
                                                            .values('name')[:1])).order_by('-created')
            else:
                if PaymentLog.objects.filter(outcat=4):
                    return PaymentLog.objects.filter(created__range=[startdate + " 00:00", enddate + " 23:59"],
                                                     payment_log_type='income') \
                        .annotate(counterparty_payment=Subquery(CounterParty.objects.filter(id=OuterRef('outlay'))
                                                                .select_related('user')
                                                                .values('name')[:1])).order_by('-created')
                else:
                    return PaymentLog.objects.filter(created__range=[startdate + " 00:00", enddate + " 23:59"],
                                                     payment_log_type='income').select_related('user') \
                        .order_by('-created')
        else:
            if counterparty and counterparty != 'all':
                if PaymentLog.objects.filter(outcat=4):
                    return PaymentLog.objects.filter(outcat=4, outlay__in=outlay_ids, payment_log_type='income') \
                        .annotate(counterparty_payment=Subquery(CounterParty.objects.filter(id=OuterRef('outlay'))
                                                                .select_related('user')
                                                                .values('name')[:1])).order_by('-created')
                else:
                    return PaymentLog.objects.filter(outcat=4, outlay__in=outlay_ids, payment_log_type='income') \
                        .select_related('user') \
                        .order_by('-created')
            else:
                date_now = datetime.today().date()
                if PaymentLog.objects.filter(outcat=4):
                    return PaymentLog.objects.filter(
                        created__range=[str(date_now) + " 00:00", str(date_now) + " 23:59"],
                        payment_log_type='income') \
                        .annotate(counterparty_payment=Subquery(CounterParty.objects.filter(id=OuterRef('outlay'))
                                                                .select_related('user')
                                                                .values('name')[:1])).order_by('-created')
                else:
                    return PaymentLog.objects.filter(
                        created__range=[str(date_now) + " 00:00", str(date_now) + " 23:59"],
                        payment_log_type='income').select_related('user').order_by('-created')


class ReportsOutcomePaymentsView(ListView):
    template_name = 'report_outcome_payment.html'
    model = PaymentLog
    context_object_name = 'report_outcome'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super(ReportsOutcomePaymentsView, self).get_context_data(**kwargs)
        category = self.request.GET.get('category', '')
        worker = self.request.GET.get('worker', '')
        car = self.request.GET.get('car', '')
        startdate = self.request.GET.get('startdate', None)
        enddate = self.request.GET.get('enddate', None)
        context['category_expenses'] = OutlayCategory.objects.all()
        context['selected_category'] = category
        context['startdate'] = startdate
        context['enddate'] = enddate
        context['report_outcome_form'] = ReportOutcomeForm
        if startdate and enddate:
            payments = PaymentLog.objects.filter(created__range=[startdate + " 00:00", enddate + " 23:59"],
                                                 payment_log_type='outcome').select_related('user').order_by('-created')
            if category and category != 'all':
                outlay_ids = OutLay.objects.filter(outlay_type_id=category).select_related('outlay_type') \
                    .values_list('id', flat=True)
                if worker:
                    payments = payments.filter(outlay__in=outlay_ids, outlay_child=worker)
                elif car:
                    payments = payments.filter(outlay__in=outlay_ids, outlay_child=car)
                else:
                    payments = payments.filter(outlay__in=outlay_ids)
            context['dollar_amount'] = payments.filter(payment_type='usd').aggregate(Sum('amount'))
            context['sum_amount'] = payments.filter(payment_type='uzs').aggregate(Sum('amount'))
        else:
            if category and category != 'all':
                outlay_ids = OutLay.objects.filter(outlay_type_id=category).select_related('outlay_type') \
                    .values_list('id', flat=True)
                if worker:
                    payments = PaymentLog.objects.filter(outlay__in=outlay_ids, outlay_child=worker) \
                        .select_related('user').order_by('-created')
                elif car:
                    payments = PaymentLog.objects.filter(outlay__in=outlay_ids, outlay_child=car) \
                        .select_related('user').order_by('-created')
                else:
                    payments = PaymentLog.objects.filter(outlay__in=outlay_ids).select_related('user').order_by(
                        '-created')
                context['dollar_amount'] = payments.filter(payment_type='usd', payment_log_type='outcome') \
                    .aggregate(Sum('amount'))
                context['sum_amount'] = payments.filter(payment_type='uzs', payment_log_type='outcome') \
                    .aggregate(Sum('amount'))
            else:
                date_now = datetime.today().date()
                context['dollar_amount'] = PaymentLog.objects.filter(
                    created__range=[str(date_now) + " 00:00", str(date_now) + " 23:59"],
                    payment_type='usd', payment_log_type='outcome') \
                    .order_by('-created').select_related('user').aggregate(Sum('amount'))
                context['sum_amount'] = PaymentLog.objects.filter(
                    created__range=[str(date_now) + " 00:00", str(date_now) + " 23:59"],
                    payment_type='uzs', payment_log_type='outcome') \
                    .order_by('-created').select_related('user').aggregate(Sum('amount'))
        return context

    def get_queryset(self):
        startdate = self.request.GET.get('startdate', '')
        enddate = self.request.GET.get('enddate', '')
        category = self.request.GET.get('category', '')
        worker = self.request.GET.get('worker', '')
        car = self.request.GET.get('car', '')
        if category and category != 'all':
            outlay_ids = OutLay.objects.filter(outlay_type_id=category).select_related('outlay_type') \
                .values_list('id', flat=True)
        if startdate and enddate:
            if category and category != 'all':
                if worker:
                    return PaymentLog.objects.filter(created__range=[startdate + " 00:00", enddate + " 23:59"],
                                                     payment_log_type='outcome',
                                                     outlay_child=worker,
                                                     outlay__in=outlay_ids) \
                        .annotate(outlay_payment=Subquery(OutLay.objects.filter(id=OuterRef('outlay'))
                                                          .select_related('user')
                                                          .values('outlay_type__name')[:1])).order_by('-created')
                elif car:
                    return PaymentLog.objects.filter(created__range=[startdate + " 00:00", enddate + " 23:59"],
                                                     payment_log_type='outcome',
                                                     outlay_child=car,
                                                     outlay__in=outlay_ids) \
                        .annotate(outlay_payment=Subquery(OutLay.objects.filter(id=OuterRef('outlay'))
                                                          .select_related('user')
                                                          .values('outlay_type__name')[:1])).order_by('-created')
                else:
                    return PaymentLog.objects.filter(created__range=[startdate + " 00:00", enddate + " 23:59"],
                                                     payment_log_type='outcome',
                                                     outlay__in=outlay_ids) \
                        .annotate(outlay_payment=Subquery(OutLay.objects.filter(id=OuterRef('outlay'))
                                                          .select_related('user')
                                                          .values('outlay_type__name')[:1])).order_by('-created')
            else:
                return PaymentLog.objects.filter(created__range=[startdate + " 00:00", enddate + " 23:59"],
                                                 payment_log_type='outcome') \
                    .annotate(outlay_payment=Subquery(OutLay.objects.filter(id=OuterRef('outlay'))
                                                      .select_related('user')
                                                      .values('outlay_type__name')[:1])).order_by('-created')
        else:
            if category and category != 'all':
                if worker:
                    return PaymentLog.objects.filter(outlay__in=outlay_ids, payment_log_type='outcome',
                                                     outlay_child=worker) \
                        .annotate(outlay_payment=Subquery(OutLay.objects.filter(id=OuterRef('outlay'))
                                                          .select_related('user')
                                                          .values('outlay_type__name')[:1])).order_by('-created')
                elif car:
                    return PaymentLog.objects.filter(outlay__in=outlay_ids, payment_log_type='outcome',
                                                     outlay_child=car) \
                        .annotate(outlay_payment=Subquery(OutLay.objects.filter(id=OuterRef('outlay'))
                                                          .select_related('user')
                                                          .values('outlay_type__name')[:1])).order_by('-created')
                else:
                    return PaymentLog.objects.filter(outlay__in=outlay_ids, payment_log_type='outcome') \
                        .annotate(outlay_payment=Subquery(OutLay.objects.filter(id=OuterRef('outlay'))
                                                          .select_related('user')
                                                          .values('outlay_type__namee')[:1])).order_by('-created')
            else:
                date_now = datetime.today().date()
                return PaymentLog.objects.filter(created__range=[str(date_now) + " 00:00", str(date_now) + " 23:59"],
                                                 payment_log_type='outcome') \
                    .annotate(outlay_payment=Subquery(OutLay.objects.filter(id=OuterRef('outlay'))
                                                      .select_related('user')
                                                      .values('outlay_type__name')[:1])).order_by('-created')


class OutlayCategoryUpdate(UpdateView):
    template_name = 'outlay_category_update.html'
    model = OutlayCategory
    fields = '__all__'
    success_url = '/outlay_cat/'


class OutlayUpdate(UpdateView):
    template_name = 'outlay_update.html'
    model = OutLay
    fields = '__all__'
    success_url = '/outlay_cat/'
