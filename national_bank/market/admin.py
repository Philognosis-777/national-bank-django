from django.contrib import admin
from .models import Currency, ExchangeRate, MarketIndicator


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'is_active')
    search_fields = ('code', 'name')


@admin.register(ExchangeRate)
class ExchangeRateAdmin(admin.ModelAdmin):
    list_display = ('currency', 'buying_rate', 'selling_rate', 'recorded_at', 'source')
    list_filter = ('source', 'recorded_at')
    search_fields = ('currency__code',)


@admin.register(MarketIndicator)
class MarketIndicatorAdmin(admin.ModelAdmin):
    list_display = ('name', 'value', 'unit', 'reference_period', 'is_active')
    search_fields = ('name',)
