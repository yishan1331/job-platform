import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(_('email address'), unique=True)
    role = models.CharField(max_length=20, choices=[
        ('recruiter', 'Recruiter'),
        ('applicant', 'Applicant')
    ])
    full_name = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        db_table = 'users'
        verbose_name = _('user')
        verbose_name_plural = _('users')

class Company(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    location = models.CharField(max_length=512)
    description = models.TextField(blank=True)
    website = models.URLField(max_length=256, blank=True)
    logo_url = models.URLField(max_length=512, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_companies')
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_companies')
    modified_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='modified_companies')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'companies'
        verbose_name = _('company')
        verbose_name_plural = _('companies')

class JobPosting(models.Model):
    SALARY_TYPE_CHOICES = [
        ('annual', 'Annual'),
        ('monthly', 'Monthly'),
        ('hourly', 'Hourly'),
    ]

    JOB_TYPE_CHOICES = [
        ('full-time', 'Full Time'),
        ('part-time', 'Part Time'),
        ('internship', 'Internship'),
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
    apply_url = models.URLField(max_length=512, blank=True)
    type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='job_postings')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_jobs')
    modified_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='modified_jobs')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'job_postings'
        verbose_name = _('job posting')
        verbose_name_plural = _('job postings')
