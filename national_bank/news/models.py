from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.conf import settings


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=True)


class BaseContent(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="%(class)s_items")
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        abstract = True
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug and self.title:
            base_slug = slugify(self.title)[:200]
            slug = base_slug
            Model = self.__class__
            counter = 1
            while Model.objects.filter(slug=slug).exclude(pk=getattr(self, 'pk', None)).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        # map model name to friendly route name for announcements
        model_name = self._meta.model_name
        route_name = 'announcement' if model_name == 'verbalannouncement' else model_name
        return reverse(f'news:{route_name}-detail', kwargs={'slug': self.slug})


class PaperNews(BaseContent):
    summary = models.TextField()
    content = models.TextField()
    featured_image = models.ImageField(upload_to='news/images/', blank=True, null=True)
    document = models.FileField(upload_to='news/documents/', blank=True, null=True)

    class Meta:
        verbose_name = 'Paper News'
        verbose_name_plural = 'Paper News'


class VideoNews(BaseContent):
    description = models.TextField()
    video_file = models.FileField(upload_to='news/videos/', blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)
    duration = models.IntegerField(default=0, help_text='Duration in seconds')

    class Meta:
        verbose_name = 'Video News'
        verbose_name_plural = 'Video News'


class VerbalAnnouncement(BaseContent):
    short_description = models.TextField()
    audio_file = models.FileField(upload_to='news/audio/')
    transcript = models.TextField()
    announcement_date = models.DateField()

    class Meta:
        verbose_name = 'Verbal Announcement'
        verbose_name_plural = 'Verbal Announcements'
