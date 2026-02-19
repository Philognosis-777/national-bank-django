from django.urls import path
from . import views

app_name = 'financial_institutions'

urlpatterns = [
    # Institution types (admin)
    path('types/', views.InstitutionTypeListView.as_view(), name='type-list'),
    path('types/create/', views.InstitutionTypeCreateView.as_view(), name='type-create'),
    path('types/<int:pk>/edit/', views.InstitutionTypeUpdateView.as_view(), name='type-update'),
    path('types/<int:pk>/delete/', views.InstitutionTypeDeleteView.as_view(), name='type-delete'),

    # Institutions
    path('institutions/', views.InstitutionListView.as_view(), name='institution-list'),
    path('institutions/create/', views.InstitutionCreateView.as_view(), name='institution-create'),
    path('institutions/<slug:slug>/', views.InstitutionDetailView.as_view(), name='institution-detail'),
    path('institutions/<slug:slug>/edit/', views.InstitutionUpdateView.as_view(), name='institution-update'),
    path('institutions/<slug:slug>/delete/', views.InstitutionDeleteView.as_view(), name='institution-delete'),
    path('institutions/<slug:slug>/branches/', views.BranchListView.as_view(), name='branch-list'),
    path('institutions/<slug:slug>/branches/create/', views.BranchCreateView.as_view(), name='branch-create'),
    path('institutions/<slug:slug>/branches/<int:pk>/edit/', views.BranchUpdateView.as_view(), name='branch-update'),
    path('institutions/<slug:slug>/branches/<int:pk>/delete/', views.BranchDeleteView.as_view(), name='branch-delete'),
    path('institutions/<slug:slug>/dashboard/', views.InstitutionDashboardView.as_view(), name='institution-dashboard'),
]
