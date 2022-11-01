import uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    username = models.CharField(
        verbose_name=(_("Username")), max_length=255, unique=True
    )
    first_name = models.CharField(verbose_name=(_("First name")), max_length=50)
    last_name = models.CharField(verbose_name=(_("Last name")), max_length=50)
    email = models.EmailField(verbose_name=(_("Email address")), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    avatar = models.ImageField(upload_to="news/avatars/", null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    objects = CustomUserManager()

    class Meta:
        verbose_name = _("Admin")
        verbose_name_plural = _("Admins")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def avatar_url(self):
        try:
            url = self.avatar.url  # set this image
        except:
            url = ''  # set default image
        return url
