from django.urls import path
from . import views

app_name = 'market'

urlpatterns = [
    # Rates
    path('rates/', views.LatestRatesView.as_view(), name='rates-latest'),
    path('rates/<str:currency_code>/', views.CurrencyHistoryView.as_view(), name='rates-history'),

    # Indicators
    path('indicators/', views.IndicatorListView.as_view(), name='indicator-list'),
    path('indicators/create/', views.IndicatorCreateView.as_view(), name='indicator-create'),
    path('indicators/<int:pk>/', views.IndicatorDetailView.as_view(), name='indicator-detail'),
    path('indicators/<int:pk>/edit/', views.IndicatorUpdateView.as_view(), name='indicator-update'),
    path('indicators/<int:pk>/delete/', views.IndicatorDeleteView.as_view(), name='indicator-delete'),

    path('dashboard/market-summary/', views.DashboardMarketSummaryView.as_view(), name='dashboard-market-summary'),
]
