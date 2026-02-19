"""
URL configuration for national_bank project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls', namespace='core')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    # News backend routes (paper, video, announcements)
    path('', include('news.urls', namespace='news')),
    # Market app routes (rates and indicators)
    path('', include('market.urls', namespace='market')),
    # Financial institutions routes (types, institutions, branches)
    path('', include('financial_institutions.urls', namespace='financial_institutions')),
    # Dashboard routes (under /dashboard/ to avoid conflict with Django admin)
    path('dashboard/', include('dashboard.urls', namespace='dashboard')),
    # Notifications
    path('', include('notifications.urls', namespace='notifications')),
]
 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
