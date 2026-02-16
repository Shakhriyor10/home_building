from django.urls import path

from counter_party.views import CounterPartyView, CounterPartyCreateView, CounterPartyDetailView, CounterPartyUpdate

urlpatterns = [
    path('counter_party/list', CounterPartyView.as_view(), name='counter_party'),
    path('counter_party/create', CounterPartyCreateView.as_view(), name='counter_party_create'),
    path('counter_party/detail/<int:pk>/', CounterPartyDetailView.as_view(), name='counter_party_detail'),
    path('counter_party/update/<int:pk>/', CounterPartyUpdate.as_view(), name='counter_party_update')
]
