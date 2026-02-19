from django.core.management.base import BaseCommand, CommandError
from market.services import update_exchange_rates_from_api, APIError


class Command(BaseCommand):
    help = 'Fetch latest exchange rates from configured API and update the database.'

    def handle(self, *args, **options):
        try:
            result = update_exchange_rates_from_api()
            self.stdout.write(self.style.SUCCESS(f"Rates updated: {result}"))
        except APIError as exc:
            raise CommandError(f"API error: {exc}")
        except Exception as exc:
            raise CommandError(f"Unexpected error: {exc}")
