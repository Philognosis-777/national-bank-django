from django.views.generic import TemplateView
from .models import VideoNews, PaperNews, VerbalAnnouncement
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView

class NewsDashboardView(TemplateView):
    template_name = "news/news_dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["videos"] = VideoNews.objects.all().order_by("-created_at")
        context["paper_news"] = PaperNews.objects.all().order_by("-created_at")
        context["announcements"] = VerbalAnnouncement.objects.all().order_by("-created_at")

        return context
class VideoNewsDetailView(DetailView):
    model = VideoNews
    template_name = "news/videonews_detail.html"
    context_object_name = "video_news"

class PaperNewsDetailView(DetailView):
    model = PaperNews
    template_name = "news/papernews_detail.html"
    context_object_name = "paper_news"

class VerbalAnnouncementDetailView(DetailView):
    model = VerbalAnnouncement
    template_name = "news/verbalannouncement_detail.html"
    context_object_name = "announcement"

class VideoNewsCreateView(CreateView):
    model = VideoNews
    fields = ['video_file', 'description', 'video_url', 'duration']
    template_name = "news/videonews_form.html"
    success_url = "/dashboard/news/"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class VideoNewsUpdateView(UpdateView):
    model = VideoNews
    fields = ['video_file', 'description', 'video_url', 'duration']
    template_name = "news/videonews_form.html"
    success_url = "/dashboard/news/"

class VideoNewsDeleteView(DeleteView):
    model = VideoNews
    template_name = "news/videonews_confirm_delete.html"
    success_url = "/dashboard/news/"


class PaperNewsCreateView(CreateView):
    model = PaperNews
    fields = ['summary', 'content', 'featured_image', 'document']
    template_name = "news/papernews_form.html"
    success_url = "/dashboard/news/"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PaperNewsUpdateView(UpdateView):
    model = PaperNews
    fields = ['summary', 'content', 'featured_image', 'document']
    template_name = "news/papernews_form.html"
    success_url = "/dashboard/news/"

class PaperNewsDeleteView(DeleteView):
    model = PaperNews
    template_name = "news/papernews_confirm_delete.html"
    success_url = "/dashboard/news/"


class VerbalAnnouncementCreateView(CreateView):
    model = VerbalAnnouncement
    fields = ['short_description', 'audio_file', 'transcript', 'announcement_date']
    template_name = "news/verbalannouncement_form.html"
    success_url = "/dashboard/news/"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class VerbalAnnouncementUpdateView(UpdateView):
    model = VerbalAnnouncement
    fields = ['short_description', 'audio_file', 'transcript', 'announcement_date']
    template_name = "news/verbalannouncement_form.html"
    success_url = "/dashboard/news/"

class VerbalAnnouncementDeleteView(DeleteView):
    model = VerbalAnnouncement
    template_name = "news/verbalannouncement_confirm_delete.html"
    success_url = "/dashboard/news/"
    