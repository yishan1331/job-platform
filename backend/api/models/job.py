import uuid

from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField
from django.db import models
from django.db.models import Q, UniqueConstraint
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .company import Company
from .user import User


class JobPostingManager(models.Manager):
    def exists_duplicate_title(self, company, title):
        return self.filter(company=company, title=title, is_active=True).exists()


class JobPosting(models.Model):
    objects = JobPostingManager()

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
    min_salary = models.IntegerField(null=True, blank=True)
    max_salary = models.IntegerField(null=True, blank=True)
    salary_type = models.CharField(max_length=10, choices=SALARY_TYPE_CHOICES)
    required_skills = models.JSONField()
    posting_date = models.DateTimeField()
    expiration_date = models.DateTimeField(null=True, blank=True)
    apply_url = models.URLField(max_length=512, null=True, blank=True)
    type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="job_postings")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_jobs")
    modified_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="modified_jobs")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    company_name_cached = models.CharField(max_length=100, editable=False)

    @property
    def company_name(self) -> str:
        return self.company.name

    @property
    def is_expired(self):
        return self.expiration_date and timezone.now() > self.expiration_date

    class Meta:
        db_table = "job_postings"
        verbose_name = _("job posting")
        verbose_name_plural = _("job postings")
        ordering = ["-posting_date"]
        indexes = [
            GinIndex(fields=["search_vector"]),  # 全文搜尋的 GIN 索引
            models.Index(fields=["company"]),
            models.Index(fields=["is_active"]),
            models.Index(fields=["expiration_date"]),
            models.Index(fields=["posting_date"]),
        ]
        constraints = [
            UniqueConstraint(
                fields=["company", "title"],
                condition=Q(is_active=True),
                name="unique_active_job_title_per_company",
            )
        ]

    search_vector = SearchVectorField(null=True)
