from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import TemplateView
from django.utils import timezone
from datetime import timedelta
from .models import Currency
import json

class MarketPageView(TemplateView):
    template_name = 'market/market.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pass currencies for initial render (optional, JS will fetch)
        context['currencies'] = Currency.objects.all()
        return context