from django.urls import path

from product.views import ProductView, ProductCreate, ProductUpdate, ProductReport

urlpatterns = [
    path('', ProductView.as_view(), name='product'),
    path('product_create/', ProductCreate.as_view(), name='product_create'),
    path('product_update/<int:pk>/', ProductUpdate.as_view(), name='product_update'),
    path('product_report/', ProductReport.as_view(), name='product_report')
]
