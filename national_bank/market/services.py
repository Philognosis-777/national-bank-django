import os
import logging
from decimal import Decimal
from typing import Optional, Dict, Any

import requests
from django.db import transaction
from django.utils import timezone

from .models import Currency, ExchangeRate

logger = logging.getLogger(__name__)


class APIError(Exception):
    pass


def fetch_exchange_rates(api_url: Optional[str] = None, api_key: Optional[str] = None, timeout: int = 10) -> Dict[str, Any]:
    """Fetch raw data from external API. Returns parsed JSON/dict.

    Uses `api_url` if provided, otherwise reads `MARKET_API_URL` from env.
    Uses `api_key` from env if not provided.
    """
    api_url = api_url or os.getenv('MARKET_API_URL')
    api_key = api_key or os.getenv('MARKET_API_KEY')

    if not api_url:
        raise APIError('No API url configured (MARKET_API_URL)')

    headers = {}
    if api_key:
        headers['Authorization'] = f'Bearer {api_key}'

    try:
        resp = requests.get(api_url, headers=headers, timeout=timeout)
        resp.raise_for_status()
    except requests.RequestException as exc:
        logger.exception('Exchange rates API request failed')
        raise APIError(str(exc))

    try:
        data = resp.json()
    except ValueError:
        logger.exception('Invalid JSON from exchange rates API')
        raise APIError('Invalid JSON response')

    return data


def validate_rate_item(item: dict) -> dict:
    """Validate a single item from API and normalize keys.

    Expected minimal keys: code, buying, selling [, middle] [, recorded_at]
    """
    required = ('code', 'buying', 'selling')
    for key in required:
        if key not in item:
            raise APIError(f'Missing key {key} in item')

    return item


def update_exchange_rates_from_api(api_url: Optional[str] = None, api_key: Optional[str] = None) -> Dict[str, int]:
    """Fetch rates and persist them. Returns summary: {created: n, updated: m}.

    This function keeps API logic in services layer, uses DB transaction per batch,
    and is resilient to partial failures (logs them, raises APIError on fetch failure).
    """
    data = fetch_exchange_rates(api_url=api_url, api_key=api_key)

    items = data.get('rates') if isinstance(data, dict) else None
    if items is None:
        raise APIError('Unexpected API payload structure: expected top-level "rates"')

    created = 0
    updated = 0
    errors = 0

    with transaction.atomic():
        for raw in items:
            try:
                item = validate_rate_item(raw)
                code = item.get('code')
                buying = Decimal(str(item.get('buying')))
                selling = Decimal(str(item.get('selling')))
                middle = item.get('middle')
                middle_val = Decimal(str(middle)) if middle is not None else None
                recorded_at = item.get('recorded_at')
                if recorded_at:
                    # assume ISO format
                    recorded_at = timezone.datetime.fromisoformat(recorded_at)
                else:
                    recorded_at = timezone.now()

                currency, _ = Currency.objects.get_or_create(code=code, defaults={'name': code})

                # Use get_or_create with unique constraint; if exists, update if changed
                obj, created_flag = ExchangeRate.objects.get_or_create(
                    currency=currency, recorded_at=recorded_at,
                    defaults={
                        'buying_rate': buying,
                        'selling_rate': selling,
                        'middle_rate': middle_val,
                        'source': 'api'
                    }
                )

                if created_flag:
                    created += 1
                else:
                    changed = False
                    if obj.buying_rate != buying:
                        obj.buying_rate = buying
                        changed = True
                    if obj.selling_rate != selling:
                        obj.selling_rate = selling
                        changed = True
                    if middle_val is not None and obj.middle_rate != middle_val:
                        obj.middle_rate = middle_val
                        changed = True
                    if changed:
                        obj.source = 'api'
                        obj.save()
                        updated += 1

            except Exception as exc:
                logger.exception('Failed to process rate item: %s', raw)
                errors += 1
                continue

    return {'created': created, 'updated': updated, 'errors': errors}
