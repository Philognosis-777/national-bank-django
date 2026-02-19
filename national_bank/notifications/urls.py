from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    path('notifications/', views.NotificationListView.as_view(), name='notification-list'),
    path('notifications/<int:pk>/', views.NotificationDetailView.as_view(), name='notification-detail'),
    path('notifications/create/', views.NotificationCreateView.as_view(), name='notification-create'),
    path('notifications/<int:pk>/edit/', views.NotificationUpdateView.as_view(), name='notification-update'),
    path('notifications/<int:pk>/delete/', views.NotificationDeleteView.as_view(), name='notification-delete'),
]
