from django.db.models.signals import post_save
from django.dispatch import receiver

from api.models.company import Company
from api.models.job import JobPosting


@receiver(post_save, sender=Company)
def update_jobposting_company_name(sender, instance, **kwargs):
    # 批次更新所有與此公司相關的 JobPosting
    JobPosting.objects.filter(company=instance).update(company_name_cached=instance.name)

    if not instance.is_active:
        JobPosting.objects.filter(company=instance).update(is_active=False)
