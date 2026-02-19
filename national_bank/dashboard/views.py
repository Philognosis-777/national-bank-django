from django.http import JsonResponse
from django.views import View

from .mixins import AdminRequiredMixin
from . import services


class AdminDashboardView(AdminRequiredMixin, View):
    """Aggregate data for admin dashboard.

    Returns JSON with market, institution, news, and user summaries.
    """

    def get(self, request):
        market = services.get_latest_exchange_rates(limit=20)
        institutions = services.get_institution_summary()
        news = services.get_news_summary()
        users = services.get_user_summary()
        widgets = services.get_dashboard_config()

        payload = {
            'market': market,
            'institutions': institutions,
            'news': news,
            'users': users,
            'widgets': widgets,
            'generated_at': __import__('django.utils.timezone').utils.timezone.now().isoformat(),
        }
        return JsonResponse(payload)


class PublicDashboardView(View):
    """Limited public dashboard with non-sensitive summaries."""

    def get(self, request):
        market = services.get_latest_exchange_rates(limit=10)
        institutions = services.get_institution_summary()
        # only include non-sensitive counts
        public = {
            'institutions_active': institutions.get('active'),
            'institutions_total': institutions.get('total'),
        }
        news = services.get_news_summary()
        payload = {
            'market': market,
            'institutions': public,
            'news': news,
            'generated_at': __import__('django.utils.timezone').utils.timezone.now().isoformat(),
        }
        return JsonResponse(payload)
