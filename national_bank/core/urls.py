from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.IntroView.as_view(), name='intro'),
    path('home/', views.HomeView.as_view(), name='home'),
    path('financial-reports/', views.FinancialReportsView.as_view(), name='financial-reports'),
    path('statistics/', views.StatisticsView.as_view(), name='statistics'),
    path('economic-indicators/', views.EconomicIndicatorsView.as_view(), name='economic-indicators'),
    path('regulations/', views.RegulationsView.as_view(), name='regulations'),
    path('monetary-policy/', views.MonetaryPolicyView.as_view(), name='monetary-policy'),
    path('legal-framework/', views.LegalFrameworkView.as_view(), name='legal-framework'),
    path('history/', views.HistoryView.as_view(), name='history'),
    path('mission-vision/', views.MissionVisionView.as_view(), name='mission-vision'),
    path('organization/', views.OrganizationView.as_view(), name='organization'),
    path('branch-locator/', views.BranchLocatorView.as_view(), name='branch-locator'),
    path('faqs/', views.FAQsView.as_view(), name='faqs'),
    path('hamburger/', views.HamburgerView.as_view(), name='hamburger'),

]
