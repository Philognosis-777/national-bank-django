from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    # Admin dashboard namespace is under /dashboard/admin/
    path('adminDash', views.AdminDashboardView.as_view(), name='admin-dashboard'),
    path('admin/summary/', views.AdminDashboardView.as_view(), name='admin-summary'),
    path('admin/market-summary/', views.AdminDashboardView.as_view(), name='admin-market-summary'),
    path('admin/institution-summary/', views.AdminDashboardView.as_view(), name='admin-institution-summary'),
    path('admin/news-summary/', views.AdminDashboardView.as_view(), name='admin-news-summary'),

    # Public dashboard
    path('', views.PublicDashboardView.as_view(), name='public-dashboard'),
]
