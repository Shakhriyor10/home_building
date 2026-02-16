from django.contrib import admin

from income.models import Income, IncomeItem


@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    pass


@admin.register(IncomeItem)
class IncomeItemAdmin(admin.ModelAdmin):
    pass
