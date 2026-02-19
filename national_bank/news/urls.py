from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    # Paper
    path('paper/', views.PaperListView.as_view(), name='paper-list'),
    path('paper/create/', views.PaperCreateView.as_view(), name='paper-create'),
    path('paper/<slug:slug>/', views.PaperDetailView.as_view(), name='paper-detail'),
    path('paper/<slug:slug>/edit/', views.PaperUpdateView.as_view(), name='paper-update'),
    path('paper/<slug:slug>/delete/', views.PaperDeleteView.as_view(), name='paper-delete'),

    # Video
    path('video/', views.VideoListView.as_view(), name='video-list'),
    path('video/create/', views.VideoCreateView.as_view(), name='video-create'),
    path('video/<slug:slug>/', views.VideoDetailView.as_view(), name='video-detail'),
    path('video/<slug:slug>/edit/', views.VideoUpdateView.as_view(), name='video-update'),
    path('video/<slug:slug>/delete/', views.VideoDeleteView.as_view(), name='video-delete'),

    # Announcements (verbal)
    path('announcements/', views.AnnouncementListView.as_view(), name='announcement-list'),
    path('announcements/create/', views.AnnouncementCreateView.as_view(), name='announcement-create'),
    path('announcements/<slug:slug>/', views.AnnouncementDetailView.as_view(), name='announcement-detail'),
    path('announcements/<slug:slug>/edit/', views.AnnouncementUpdateView.as_view(), name='announcement-update'),
    path('announcements/<slug:slug>/delete/', views.AnnouncementDeleteView.as_view(), name='announcement-delete'),
    path('dashboard/news-summary/', views.DashboardNewsSummaryView.as_view(), name='dashboard-news-summary'),
]
