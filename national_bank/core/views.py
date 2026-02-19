from django.views.generic import TemplateView


class IntroView(TemplateView):
    template_name = 'core/intro.html'


class HomeView(TemplateView):
    template_name = 'core/home.html'

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