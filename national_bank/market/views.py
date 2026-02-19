from django.http import JsonResponse, Http404
from django.views.generic import View
from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Currency, ExchangeRate, MarketIndicator
from .mixins import AdminRequiredMixin


def serialize_rate(rate: ExchangeRate) -> dict:
    return {
        'currency': rate.currency.code,
        'buying_rate': str(rate.buying_rate),
        'selling_rate': str(rate.selling_rate),
        'middle_rate': str(rate.middle_rate) if rate.middle_rate is not None else None,
        'recorded_at': rate.recorded_at.isoformat(),
        'source': rate.source,
    }


class LatestRatesView(View):
    """Return latest exchange rate for each active currency as JSON."""

    def get(self, request):
        qs = Currency.objects.filter(is_active=True).order_by('code')
        results = []
        for cur in qs:
            rate = cur.rates.filter().order_by('-recorded_at').first()
            if rate is None:
                continue
            # If user is not admin, only include published-like logic not relevant here
            results.append(serialize_rate(rate))

        return JsonResponse({'results': results})


class CurrencyHistoryView(View):
    """Return historical rates for a currency. Supports pagination and simple filtering by date range via GET params."""

    def get(self, request, currency_code):
        currency = get_object_or_404(Currency, code__iexact=currency_code)
        qs = currency.rates.all().order_by('-recorded_at')

        # date filtering (optional)
        start = request.GET.get('start')
        end = request.GET.get('end')
        if start:
            try:
                start_dt = timezone.datetime.fromisoformat(start)
                qs = qs.filter(recorded_at__gte=start_dt)
            except Exception:
                pass
        if end:
            try:
                end_dt = timezone.datetime.fromisoformat(end)
                qs = qs.filter(recorded_at__lte=end_dt)
            except Exception:
                pass

        page = int(request.GET.get('page', 1))
        per_page = int(request.GET.get('per_page', 25))
        paginator = Paginator(qs, per_page)
        try:
            page_obj = paginator.page(page)
        except EmptyPage:
            return JsonResponse({'results': [], 'count': paginator.count})

        results = [serialize_rate(r) for r in page_obj.object_list]
        return JsonResponse({'results': results, 'count': paginator.count, 'num_pages': paginator.num_pages})


# MarketIndicator views (CRUD)
class IndicatorListView(View):
    def get(self, request):
        qs = MarketIndicator.objects.filter(is_active=True).order_by('name')
        q = request.GET.get('q')
        if q:
            qs = qs.filter(name__icontains=q)
        data = [{'id': i.pk, 'name': i.name, 'value': str(i.value), 'unit': i.unit, 'reference_period': i.reference_period} for i in qs]
        return JsonResponse({'results': data})


class IndicatorDetailView(View):
    def get(self, request, pk):
        indicator = get_object_or_404(MarketIndicator, pk=pk)
        data = {'id': indicator.pk, 'name': indicator.name, 'value': str(indicator.value), 'unit': indicator.unit, 'reference_period': indicator.reference_period}
        return JsonResponse(data)


class IndicatorCreateView(AdminRequiredMixin, View):
    def post(self, request):
        data = request.POST
        indicator = MarketIndicator.objects.create(
            name=data.get('name', ''),
            value=data.get('value') or 0,
            unit=data.get('unit', ''),
            reference_period=data.get('reference_period', ''),
            is_active=data.get('is_active', True),
        )
        return JsonResponse({'id': indicator.pk, 'created': True})


class IndicatorUpdateView(AdminRequiredMixin, View):
    def post(self, request, pk):
        indicator = get_object_or_404(MarketIndicator, pk=pk)
        data = request.POST
        indicator.name = data.get('name', indicator.name)
        indicator.value = data.get('value', indicator.value)
        indicator.unit = data.get('unit', indicator.unit)
        indicator.reference_period = data.get('reference_period', indicator.reference_period)
        indicator.is_active = data.get('is_active', indicator.is_active)
        indicator.save()
        return JsonResponse({'id': indicator.pk, 'updated': True})


class IndicatorDeleteView(AdminRequiredMixin, View):
    def post(self, request, pk):
        indicator = get_object_or_404(MarketIndicator, pk=pk)
        indicator.delete()
        return JsonResponse({'id': pk, 'deleted': True})

class DashboardMarketSummaryView(LoginRequiredMixin, View):
    """Return a summary of market data for dashboard widgets."""

    def get(self, request):
        latest_rates = []
        for cur in Currency.objects.filter(is_active=True).order_by('code'):
            rate = cur.rates.filter().order_by('-recorded_at').first()
            if rate:
                latest_rates.append(serialize_rate(rate))

        # For simplicity, just return the most recent rate across all currencies as a summary
        latest_rate = max(latest_rates, key=lambda r: r['recorded_at'], default=None)
        return JsonResponse({'latest_rate': latest_rate})