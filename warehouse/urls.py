from django.urls import path

from warehouse.views import WarehouseList, WarehouseCreate, WarehouseUpdate, OtherActionView

urlpatterns = [
    path('warehouse/', WarehouseList.as_view(), name='warehouse_list'),
    path('warehouse_create/', WarehouseCreate.as_view(), name='warehouse_create'),
    path('warehouse_update/<int:pk>/', WarehouseUpdate.as_view(), name='warehouse_update'),
    path('other/action/', OtherActionView.as_view(), name='other_action'),
]
