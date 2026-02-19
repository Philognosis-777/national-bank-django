from django.db import models


class DashboardConfig(models.Model):
    widget_name = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order', 'widget_name']

    def __str__(self):
        return f"{self.display_order} - {self.widget_name}"
