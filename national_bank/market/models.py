from django.db import models
from django.utils import timezone


class Currency(models.Model):
    code = models.CharField(max_length=8, unique=True)
    name = models.CharField(max_length=128)
    symbol = models.CharField(max_length=16, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['code']
        indexes = [
            models.Index(fields=['code']),
        ]

    def __str__(self):
        return f"{self.code} - {self.name}"


class ExchangeRate(models.Model):
    SOURCE_CHOICES = [
        ('api', 'API'),
        ('manual', 'Manual'),
    ]

    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='rates')
    buying_rate = models.DecimalField(max_digits=20, decimal_places=6)
    selling_rate = models.DecimalField(max_digits=20, decimal_places=6)
    middle_rate = models.DecimalField(max_digits=20, decimal_places=6, blank=True, null=True)
    source = models.CharField(max_length=16, choices=SOURCE_CHOICES, default='api')
    recorded_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-recorded_at']
        indexes = [
            models.Index(fields=['currency', 'recorded_at']),
        ]
        constraints = [
            models.UniqueConstraint(fields=['currency', 'recorded_at'], name='unique_currency_recorded_at')
        ]

    def __str__(self):
        return f"{self.currency.code} @ {self.recorded_at:%Y-%m-%d %H:%M}"


class MarketIndicator(models.Model):
    name = models.CharField(max_length=128)
    value = models.DecimalField(max_digits=20, decimal_places=6)
    unit = models.CharField(max_length=32, blank=True)
    reference_period = models.CharField(max_length=64, blank=True)
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return f"{self.name}: {self.value} {self.unit or ''}".strip()
