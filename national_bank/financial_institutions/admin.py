from django.contrib import admin
from .models import InstitutionType, FinancialInstitution, Branch


@admin.register(InstitutionType)
class InstitutionTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(FinancialInstitution)
class FinancialInstitutionAdmin(admin.ModelAdmin):
    list_display = ('name', 'institution_type', 'license_number', 'status', 'is_supervised')
    search_fields = ('name', 'license_number')
    list_filter = ('status', 'institution_type')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('branch_name', 'institution', 'city', 'region', 'is_active')
    search_fields = ('branch_name', 'city', 'region')
