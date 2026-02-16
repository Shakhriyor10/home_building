from django.contrib import admin

from payment.models import Car, Workers, OutlayCategory, OutLay, PaymentLog, Cashier, ProjectSetting


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    pass


@admin.register(Workers)
class WorkersAdmin(admin.ModelAdmin):
    pass


@admin.register(OutlayCategory)
class OutlayCategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(OutLay)
class OutLayAdmin(admin.ModelAdmin):
    pass


@admin.register(PaymentLog)
class PaymentLogAdmin(admin.ModelAdmin):
    pass


@admin.register(Cashier)
class CashierAdmin(admin.ModelAdmin):
    pass


@admin.register(ProjectSetting)
class ProjectSettingAdmin(admin.ModelAdmin):
    pass
