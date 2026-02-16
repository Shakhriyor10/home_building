from django.contrib import admin

from counter_party.models import CounterParty


@admin.register(CounterParty)
class CounterPartyAdmin(admin.ModelAdmin):
    pass
