from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = models.CharField(null=True, blank=True)  # optional username
    email = models.EmailField('email address', unique=True)

    ROLE_ADMIN = 'admin'
    ROLE_PUBLIC = 'public'
    ROLE_CHOICES = [
        (ROLE_ADMIN, 'Admin'),
        (ROLE_PUBLIC, 'Public'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_PUBLIC)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # no extra required fields

    objects = CustomUserManager()  # ← use custom manager

    def __str__(self):
        return self.email
