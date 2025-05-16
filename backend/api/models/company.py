import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from .user import User


class Company(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    location = models.CharField(max_length=512)
    description = models.TextField(blank=True)
    website = models.URLField(max_length=256, blank=True)
    logo_url = models.URLField(max_length=512, blank=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="owned_companies"
    )
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="created_companies"
    )
    modified_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="modified_companies"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "companies"
        verbose_name = _("company")
        verbose_name_plural = _("companies")
