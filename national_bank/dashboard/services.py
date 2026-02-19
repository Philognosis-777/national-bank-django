from typing import Dict, Any
from django.db.models import Count
from django.contrib.auth import get_user_model
from django.utils import timezone

from market.models import ExchangeRate, Currency
from financial_institutions.models import FinancialInstitution
from news.models import PaperNews, VideoNews, VerbalAnnouncement
from .models import DashboardConfig


def get_latest_exchange_rates(limit: int = 10) -> Dict[str, Any]:
    """Return latest rates per currency. Efficient: group by currency and pick latest."""
    results = []
    # For each active currency, pick latest rate
    qs = Currency.objects.filter(is_active=True).order_by('code')
    for cur in qs:
        rate = cur.rates.order_by('-recorded_at').first()
        if not rate:
            continue
        results.append({
            'currency': cur.code,
            'buying_rate': str(rate.buying_rate),
            'selling_rate': str(rate.selling_rate),
            'middle_rate': str(rate.middle_rate) if rate.middle_rate is not None else None,
            'recorded_at': rate.recorded_at.isoformat(),
        })
        if len(results) >= limit:
            break
    return {'results': results}


def get_institution_summary() -> Dict[str, int]:
    total = FinancialInstitution.objects.count()
    active = FinancialInstitution.objects.filter(status=FinancialInstitution.STATUS_ACTIVE).count()
    suspended = FinancialInstitution.objects.filter(status=FinancialInstitution.STATUS_SUSPENDED).count()
    revoked = FinancialInstitution.objects.filter(status=FinancialInstitution.STATUS_REVOKED).count()
    supervised = FinancialInstitution.objects.filter(is_supervised=True).count()
    return {
        'total': total,
        'active': active,
        'suspended': suspended,
        'revoked': revoked,
        'supervised': supervised,
    }


def get_news_summary() -> Dict[str, int]:
    # count published items across models
    paper = PaperNews.published.count() if hasattr(PaperNews, 'published') else PaperNews.objects.filter(is_published=True).count()
    video = VideoNews.published.count() if hasattr(VideoNews, 'published') else VideoNews.objects.filter(is_published=True).count()
    verbal = VerbalAnnouncement.published.count() if hasattr(VerbalAnnouncement, 'published') else VerbalAnnouncement.objects.filter(is_published=True).count()
    return {'paper_published': paper, 'video_published': video, 'verbal_published': verbal}


def get_user_summary() -> Dict[str, int]:
    User = get_user_model()
    total = User.objects.count()
    admin = User.objects.filter(is_superuser=True).count() + User.objects.filter(role='admin').count()
    public = total - admin
    return {'total_users': total, 'admin_users': admin, 'public_users': public}


def get_dashboard_config() -> list:
    return list(DashboardConfig.objects.filter(is_active=True).order_by('display_order').values('widget_name', 'display_order'))
