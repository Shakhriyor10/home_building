from django.urls import path

from income.views import IncomeListView, IncomeCreateView, IncomeDetailView, IncomeActionView

urlpatterns = [
    path('income_list/', IncomeListView.as_view(), name='income_list'),
    path('income_create/', IncomeCreateView.as_view(), name='income_create'),
    path('income_detail/<int:pk>/', IncomeDetailView.as_view(), name='income_detail'),
    path('income_action/<int:pk>/', IncomeActionView.as_view(), name='income_actions'),
]
