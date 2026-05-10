from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    class Role(models.TextChoices):
        SUPER_ADMIN = 'super_admin'
        USER = 'user'

    role = models.CharField(max_length=20, choices=Role.choices, default=Role.USER)
    phone = models.CharField(max_length=20, blank=True)
    is_verified = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.role == self.Role.SUPER_ADMIN:
           if User.objects.filter(role=self.Role.SUPER_ADMIN).exclude(pk=self.pk).exists():
               raise ValueError("Only one super admin is allowed.")
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.username