from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    # News dashboard
    path('news/', views.NewsDashboardView.as_view(), name='news'),
    path('videos/<int:pk>/', views.VideoNewsDetailView.as_view(), name='video-news-detail'),
    path('papers/<int:pk>/', views.PaperNewsDetailView.as_view(), name='paper-news-detail'),
    path('announcements/<int:pk>/', views.VerbalAnnouncementDetailView.as_view(), name='verbal-announcement-detail'),
    path('videos/create/', views.VideoNewsCreateView.as_view(), name='video-news-create'),
    path('videos/<int:pk>/update/', views.VideoNewsUpdateView.as_view(), name='video-news-update'),
    path('videos/<int:pk>/delete/', views.VideoNewsDeleteView.as_view(), name='video-news-delete'),
    path('papers/create/', views.PaperNewsCreateView.as_view(), name='paper-news-create'),
    path('papers/<int:pk>/update/', views.PaperNewsUpdateView.as_view(), name='paper-news-update'),
    path('papers/<int:pk>/delete/', views.PaperNewsDeleteView.as_view(), name='paper-news-delete'),
    path('announcements/create/', views.VerbalAnnouncementCreateView.as_view(), name='verbal-announcement-create'),
    path('announcements/<int:pk>/update/', views.VerbalAnnouncementUpdateView.as_view(), name='verbal-announcement-update'),
    path('announcements/<int:pk>/delete/', views.VerbalAnnouncementDeleteView.as_view(), name='verbal-announcement-delete'),
]
