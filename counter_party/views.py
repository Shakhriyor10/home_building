from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView, CreateView, TemplateView, UpdateView

from counter_party.models import CounterParty


class CounterPartyView(ListView):
    template_name = 'counter_party_list.html'
    model = CounterParty

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CounterPartyView, self).get_context_data(**kwargs)
        context['contr_agents'] = CounterParty.objects.all
        return context


class CounterPartyCreateView(CreateView):
    template_name = 'counter_party_create.html'
    model = CounterParty
    fields = ['name', 'org_name', 'phone', 'phone2', 'address', 'inn', 'email', 'status', 'sms_live', 'extra_info',
              'user']
    success_url = '/counter_party/list'


class CounterPartyDetailView(TemplateView):
    template_name = 'counter_party_detail.html'

    def get_context_data(self, **kwargs):
        context = super(CounterPartyDetailView, self).get_context_data(**kwargs)
        counter_party = CounterParty.objects.get(id=self.kwargs['pk'])
        context['contr_agent'] = counter_party
        return context


class CounterPartyUpdate(UpdateView):
    template_name = 'counter_party_update.html'
    model = CounterParty
    fields = ['name', 'org_name', 'phone', 'phone2', 'address', 'inn', 'email', 'status', 'sms_live', 'extra_info',
              'user']
    success_url = '/counter_party/list'

    def get_success_url(self):
        back_url = self.request.GET.get('back_url', None)
        pk = self.request.GET.get('pk', None)
        if back_url and pk:
            return reverse(back_url, kwargs={'pk': pk})
        elif back_url:
            return reverse(back_url)
        else:
            return reverse('counter_party')
