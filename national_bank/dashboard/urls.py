from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.DashboardView.as_view(), name='admin-dashboard'),
    path('institutions/', views.InstitutionDashboardView.as_view(), name='institution-dashboard'),
    path('news/', views.NewsDashboardView.as_view(), name='news-dashboard'),
]
