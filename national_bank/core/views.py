from multiprocessing import context

from django.views.generic import TemplateView

from news.models import VerbalAnnouncement
    
from financial_institutions.models import InstitutionType, FinancialInstitution, Branch

from market.models import Currency

from news.models import VideoNews, PaperNews, VerbalAnnouncement
class IntroView(TemplateView):
    template_name = 'core/intro.html'


class HomeView(TemplateView):
    template_name = 'core/home.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["announcements"] = VerbalAnnouncement.objects.all().order_by("-created_at")
        return context  

class FinancialReportsView(TemplateView):
    template_name = 'core/financial_reports.html'

class StatisticsView(TemplateView):
    template_name = 'core/statistics.html'

class EconomicIndicatorsView(TemplateView):
    template_name = 'core/economic_indicators.html'

class RegulationsView(TemplateView):
    template_name = 'core/regulation.html'


class MonetaryPolicyView(TemplateView):
    template_name = 'core/monetary_policy.html'

class LegalFrameworkView(TemplateView):
    template_name = 'core/legal_framework.html'

class HistoryView(TemplateView):
    template_name = 'core/history.html'

class MissionVisionView(TemplateView):
    template_name = 'core/mission_and_vision.html'


class OrganizationView(TemplateView):
    template_name = 'core/organization.html'

class BranchLocatorView(TemplateView):
    template_name = 'core/branch_locator.html'

class FAQsView(TemplateView):
    template_name = 'core/faqs.html'

class HamburgerView(TemplateView):
    template_name = 'core/hamburger.html'

class DashboardView(TemplateView):
    template_name = 'core/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["announcements"] = VerbalAnnouncement.objects.all().order_by("-created_at")
        context["institution_types"] = InstitutionType.objects.all()
        context["institutions"] = FinancialInstitution.objects.all()
        context["branches"] = Branch.objects.all()
        context['currencies'] = Currency.objects.all()
        return context