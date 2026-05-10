from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.urls import reverse


class InstitutionType(models.Model):
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class FinancialInstitution(models.Model):
    STATUS_ACTIVE = 'active'
    STATUS_SUSPENDED = 'suspended'
    STATUS_REVOKED = 'revoked'
    STATUS_CHOICES = [
        (STATUS_ACTIVE, 'Active'),
        (STATUS_SUSPENDED, 'Suspended'),
        (STATUS_REVOKED, 'Revoked'),
    ]

    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    institution_type = models.ForeignKey(InstitutionType, on_delete=models.PROTECT, related_name='institutions')
    license_number = models.CharField(max_length=64, unique=True)
    established_date = models.DateField(blank=True, null=True)
    head_office_address = models.TextField(blank=True)
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=32, blank=True)

    capital_amount = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default=STATUS_ACTIVE)
    is_supervised = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['license_number']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug and self.name:
            base = slugify(self.name)[:200]
            slug = base
            counter = 1
            while FinancialInstitution.objects.filter(slug=slug).exclude(pk=getattr(self, 'pk', None)).exists():
                slug = f"{base}-{counter}"
                counter += 1
            self.slug = slug
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('financial_institutions:institution-detail', kwargs={'slug': self.slug})


class Branch(models.Model):
    institution = models.ForeignKey(FinancialInstitution, on_delete=models.CASCADE, related_name='branches')
    branch_name = models.CharField(max_length=255)
    region = models.CharField(max_length=128, blank=True)
    city = models.CharField(max_length=128, blank=True)
    address = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['branch_name']

    def __str__(self):
        return f"{self.branch_name} ({self.institution.name})"
