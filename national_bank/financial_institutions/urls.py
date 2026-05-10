from django.urls import path
from . import views

app_name = 'financial_institutions'

urlpatterns = [
    path('institutions/', views.InstitutionPageView.as_view(), name='institution-page'),
    path('institutions/<int:pk>/', views.InstitutionDetailView.as_view(), name='institution-detail'),
    path('institutions/create/', views.InstitutionCreateView.as_view(), name='institution-create'),
    path('institutions/<int:pk>/update/', views.InstitutionUpdateView.as_view(), name='institution-update'),
    path('institutions/<int:pk>/delete/', views.InstitutionDeleteView.as_view(), name='institution-delete'),
    path('branches/<int:pk>/', views.BranchDetailView.as_view(), name='branch-detail'),
    path('branches/create/', views.BranchCreateView.as_view(), name='branch-create'),
    path('branches/<int:pk>/update/', views.BranchUpdateView.as_view(), name='branch-update'),
    path('branches/<int:pk>/delete/', views.BranchDeleteView.as_view(), name='branch-delete'),
    path('institution-types/<int:pk>/', views.InstitutionTypeDetailView.as_view(), name='institution-type-detail'),
    path('institution-types/create/', views.InstitutionTypeCreateView.as_view(), name='institution-type-create'),
    path('institution-types/<int:pk>/update/', views.InstitutionTypeUpdateView.as_view(), name='institution-type-update'),
    path('institution-types/<int:pk>/delete/', views.InstitutionTypeDeleteView.as_view(), name='institution-type-delete'),

]

