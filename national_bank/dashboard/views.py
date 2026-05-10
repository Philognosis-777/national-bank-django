from news.models import VideoNews, PaperNews, VerbalAnnouncement
from django.views.generic import TemplateView
from financial_institutions.models import InstitutionType, FinancialInstitution, Branch
from market.models import Currency

class DashboardView(TemplateView):
    template_name = "dashboard/admin_dashboard.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["videos"] = VideoNews.objects.all().order_by("-created_at")
        context["paper_news"] = PaperNews.objects.all().order_by("-created_at")
        context["announcements"] = VerbalAnnouncement.objects.all().order_by("-created_at")
        context["institution_types"] = InstitutionType.objects.all()
        context["institutions"] = FinancialInstitution.objects.all()
        context["branches"] = Branch.objects.all()
        context["currencies"] = Currency.objects.all()
        return context



class InstitutionDashboardView(TemplateView):
    template_name = "dashboard/institution_dashboard.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["institution_types"] = InstitutionType.objects.all()
        context["institutions"] = FinancialInstitution.objects.all()
        context["branches"] = Branch.objects.all()
        return context

class NewsDashboardView(TemplateView):
    template_name = "dashboard/news_dashboard.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["videos"] = VideoNews.objects.all().order_by("-created_at")
        context["paper_news"] = PaperNews.objects.all().order_by("-created_at")
        context["announcements"] = VerbalAnnouncement.objects.all().order_by("-created_at")
        return context

