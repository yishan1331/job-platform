import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from .company import Company
from .user import User


class JobPosting(models.Model):
    SALARY_TYPE_CHOICES = [
        ("annual", "Annual"),
        ("monthly", "Monthly"),
        ("hourly", "Hourly"),
    ]

    JOB_TYPE_CHOICES = [
        ("full-time", "Full Time"),
        ("part-time", "Part Time"),
        ("internship", "Internship"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=64)
    description = models.TextField()
    location = models.CharField(max_length=512)
    salary_range = models.JSONField()
    salary_type = models.CharField(max_length=10, choices=SALARY_TYPE_CHOICES)
    required_skills = models.JSONField()
    posting_date = models.DateTimeField()
    expiration_date = models.DateTimeField(null=True, blank=True)
    apply_url = models.URLField(max_length=512, null=True, blank=True)
    type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES, blank=True)
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="job_postings"
    )
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="created_jobs"
    )
    modified_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="modified_jobs"
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    @property
    def company_name(self) -> str:
        return self.company.name

    class Meta:
        db_table = "job_postings"
        verbose_name = _("job posting")
        verbose_name_plural = _("job postings")
