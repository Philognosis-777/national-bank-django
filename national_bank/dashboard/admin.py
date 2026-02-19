from django.contrib import admin
from .models import DashboardConfig


@admin.register(DashboardConfig)
class DashboardConfigAdmin(admin.ModelAdmin):
    list_display = ('widget_name', 'is_active', 'display_order')
    list_editable = ('is_active', 'display_order')
    ordering = ('display_order',)
