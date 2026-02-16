from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView
from warehouse.helpers import change_rate, conversion_balance
from warehouse.models import Warehouse


class WarehouseList(ListView):
    template_name = 'warehouse_list.html'
    model = Warehouse
    context_object_name = 'warehouses'
    queryset = Warehouse.objects.order_by('-id')


class WarehouseCreate(CreateView):
    template_name = 'warehouse_create.html'
    model = Warehouse
    fields = '__all__'
    success_url = '/warehouse/'


class WarehouseUpdate(UpdateView):
    template_name = 'warehouse_update.html'
    model = Warehouse
    fields = '__all__'
    success_url = '/warehouse/'


class OtherActionView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(OtherActionView, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        post_request = self.request.POST
        user_request = self.request.user
        action = post_request.get('action', None)
        actions = {
            'change_rate': change_rate,
            'conversion_balance': conversion_balance,
        }
        response = actions[action](post_request, user_request)
        back_url = response.get('back_url', None)
        if action == 'change_rate' or action == 'domain_info' or action == 'conversion_balance':
            return JsonResponse(response, safe=False)
        else:
            return redirect(back_url)


def handler404(request, exception):
    return render(request, 'layouts/')
