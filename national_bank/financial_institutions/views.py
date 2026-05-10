from .models import InstitutionType, FinancialInstitution, Branch
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView

class InstitutionPageView(TemplateView):
    template_name = "financial_institutions/institution.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["institution_types"] = InstitutionType.objects.all()
        context["institutions"] = FinancialInstitution.objects.all()
        context["branches"] = Branch.objects.all()
        return context

class InstitutionDetailView(DetailView):
    model = FinancialInstitution
    template_name = "financial_institutions/institutions_detail.html"
    context_object_name = "institution"

class InstitutionCreateView(CreateView):
    model = FinancialInstitution
    fields = ['name', 'institution_type', 'license_number', 'established_date', 'head_office_address','contact_email', 'contact_phone', 'capital_amount', 'status']
    template_name = "financial_institutions/institutions_form.html"
    success_url = "/dashboard/institutions/"

class InstitutionUpdateView(UpdateView):
    model = FinancialInstitution
    fields = ['name', 'institution_type', 'license_number', 'established_date', 'head_office_address', 'contact_email', 'contact_phone','capital_amount', 'status']
    template_name = "financial_institutions/institutions_form.html"
    success_url = "/dashboard/institutions/"

class InstitutionDeleteView(DeleteView):
    model = FinancialInstitution
    template_name = "financial_institutions/institutions_confirm_delete.html"
    success_url = "/dashboard/institutions/"

class BranchDetailView(DetailView):
    model = Branch
    template_name = "financial_institutions/branch_detail.html"
    context_object_name = "branch"

class BranchCreateView(CreateView):
    model = Branch
    fields = ['branch_name', 'institution', 'city', 'region', 'address']
    template_name = "financial_institutions/branch_form.html"
    success_url = "/dashboard/institutions/"

class BranchUpdateView(UpdateView):
    model = Branch
    fields = ['branch_name', 'institution', 'city', 'region', 'address']
    template_name = "financial_institutions/branch_form.html"
    success_url = "/dashboard/institutions/"  

class BranchDeleteView(DeleteView):
    model = Branch
    template_name = "financial_institutions/branch_confirm_delete.html"
    success_url = "/dashboard/institutions/"

class InstitutionTypeDetailView(DetailView):
    model = InstitutionType
    template_name = "financial_institutions/institution_type_detail.html"
    context_object_name = "institution_type"

class InstitutionTypeCreateView(CreateView):
    model = InstitutionType
    fields = ['name', 'description']
    template_name = "financial_institutions/institution_type_form.html"
    success_url = "/dashboard/institutions/"

class InstitutionTypeUpdateView(UpdateView):
    model = InstitutionType
    fields = ['name', 'description']
    template_name = "financial_institutions/institution_type_form.html"
    success_url = "/dashboard/institutions/"

class InstitutionTypeDeleteView(DeleteView):
    model = InstitutionType
    template_name = "financial_institutions/institution_type_confirm_delete.html"
    success_url = "/dashboard/institutions/"