from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import AdminRequiredMixin
from .models import PaperNews, VideoNews, VerbalAnnouncement


class BaseContentListView(ListView):
    paginate_by = 10

    def get_queryset(self):
        qs = self.model.objects.all()
        user = self.request.user
        if not (user.is_authenticated and (getattr(user, 'role', None) == 'admin' or user.is_superuser)):
            # public: only published
            # use published manager if available
            if hasattr(self.model, 'published'):
                qs = self.model.published.all()
            else:
                qs = qs.filter(is_published=True)

        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(title__icontains=q)
        return qs


class BaseContentDetailView(DetailView):
    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if not (user.is_authenticated and (getattr(user, 'role', None) == 'admin' or user.is_superuser)):
            qs = qs.filter(is_published=True)
        return qs


class BaseContentCreateView(AdminRequiredMixin, CreateView):
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class BaseContentUpdateView(AdminRequiredMixin, UpdateView):
    pass


class BaseContentDeleteView(AdminRequiredMixin, DeleteView):
    pass


# Paper views
class PaperListView(BaseContentListView):
    model = PaperNews


class PaperDetailView(BaseContentDetailView):
    model = PaperNews


class PaperCreateView(BaseContentCreateView):
    model = PaperNews
    fields = ['title', 'slug', 'is_published', 'summary', 'content', 'featured_image', 'document']


class PaperUpdateView(BaseContentUpdateView):
    model = PaperNews
    fields = ['title', 'slug', 'is_published', 'summary', 'content', 'featured_image', 'document']
    def get_success_url(self):
        return reverse_lazy('news:paper-detail', kwargs={'slug': self.object.slug})


class PaperDeleteView(BaseContentDeleteView):
    model = PaperNews
    success_url = reverse_lazy('news:paper-list')


# Video views
class VideoListView(BaseContentListView):
    model = VideoNews


class VideoDetailView(BaseContentDetailView):
    model = VideoNews


class VideoCreateView(BaseContentCreateView):
    model = VideoNews
    fields = ['title', 'slug', 'is_published', 'description', 'video_file', 'video_url', 'duration']


class VideoUpdateView(BaseContentUpdateView):
    model = VideoNews
    fields = ['title', 'slug', 'is_published', 'description', 'video_file', 'video_url', 'duration']
    def get_success_url(self):
        return reverse_lazy('news:video-detail', kwargs={'slug': self.object.slug})


class VideoDeleteView(BaseContentDeleteView):
    model = VideoNews
    success_url = reverse_lazy('news:video-list')


# Announcement views (verbal announcements)
class AnnouncementListView(BaseContentListView):
    model = VerbalAnnouncement


class AnnouncementDetailView(BaseContentDetailView):
    model = VerbalAnnouncement


class AnnouncementCreateView(BaseContentCreateView):
    model = VerbalAnnouncement
    fields = ['title', 'slug', 'is_published', 'short_description', 'audio_file', 'transcript', 'announcement_date']


class AnnouncementUpdateView(BaseContentUpdateView):
    model = VerbalAnnouncement
    fields = ['title', 'slug', 'is_published', 'short_description', 'audio_file', 'transcript', 'announcement_date']
    def get_success_url(self):
        return reverse_lazy('news:announcement-detail', kwargs={'slug': self.object.slug})


class AnnouncementDeleteView(BaseContentDeleteView):
    model = VerbalAnnouncement
    success_url = reverse_lazy('news:announcement-list')

class DashboardNewsSummaryView(LoginRequiredMixin, ListView):
    model = PaperNews
    template_name = 'dashboard/news_summary.html'
    context_object_name = 'news'

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if not (user.is_authenticated and (getattr(user, 'role', None) == 'admin' or user.is_superuser)):
            if hasattr(self.model, 'published'):
                qs = self.model.published.all()
            else:
                qs = qs.filter(is_published=True)
        return qs.order_by('-created_at')[:5]