from django.db import models
from django.utils import timezone

class Currency(models.Model):
    code = models.CharField(max_length=3, unique=True)          # e.g., USD, EUR
    name = models.CharField(max_length=50)                      # English name
    name_amharic = models.CharField(max_length=50, blank=True)  # Amharic name
    symbol = models.CharField(max_length=5, blank=True)         # $, €, £

    def __str__(self):
        return f"{self.code} - {self.name}"
