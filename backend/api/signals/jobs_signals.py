from django.contrib.postgres.search import SearchVector
from django.db.models.signals import post_save
from django.dispatch import receiver

from api.models.job import JobPosting  # 依你的 models 結構調整


@receiver(post_save, sender=JobPosting)
def update_search_vector_after_save(sender, instance, **kwargs):
    JobPosting.objects.filter(id=instance.id).update(
        search_vector=(SearchVector("title", weight="A") + SearchVector("description", weight="B"))
    )
