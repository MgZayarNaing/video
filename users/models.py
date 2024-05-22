# myapp/models.py

import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, phone_number, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, email, phone_number, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)
    last_activity = models.DateTimeField(null=True, blank=True)
    last_logout = models.DateTimeField(null=True, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'phone_number']

    def __str__(self):
        return self.username

    @property
    def formatted_phone_number(self):
        if self.phone_number:
            return f'+{self.phone_number}'
        return "N/A"

    @property
    def get_status(self):
        if self.last_activity:
            delta = timezone.now() - self.last_activity
            if delta.total_seconds() < 300:  # Considered online if active within the last 5 minutes
                return "Online"
        return "Offline"

    @property
    def get_duration(self):
        if self.last_logout and self.last_login:
            duration = self.last_logout - self.last_login
            total_seconds = int(duration.total_seconds())
            hours, remainder = divmod(total_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            return f'{hours}:{minutes:02}:{seconds:02}'
        return "N/A"

    @property
    def formatted_date_joined(self):
        if self.date_joined:
            return self.date_joined.strftime("%I:%M:%S %p %Y-%m-%d")
        return "N/A"

    @property
    def formatted_last_login(self):
        if self.last_login:
            return self.last_login.strftime("%I:%M:%S %p %Y-%m-%d")
        return "N/A"

    @property
    def formatted_last_logout(self):
        if self.last_logout:
            return self.last_logout.strftime("%I:%M:%S %p %Y-%m-%d")
        return "N/A"
