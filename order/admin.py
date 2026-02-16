from django.contrib import admin

from order.models import Order, OrderItem, OrderReturnItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    pass


@admin.register(OrderReturnItem)
class OrderReturnItemAdmin(admin.ModelAdmin):
    pass
