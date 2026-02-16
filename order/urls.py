from django.urls import path

from order.views import OrderList, OrderCreate, OrderUpdate, OrderDetailView, OrderActionView

urlpatterns = [
    path('order/', OrderList.as_view(), name='order'),
    path('order_create/', OrderCreate.as_view(), name='order_create'),
    path('order_update/<int:pk>/', OrderUpdate.as_view(), name='order_update'),
    path('order_detail/<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
    path('order_action/<int:pk>/', OrderActionView.as_view(), name='order_action')
]
