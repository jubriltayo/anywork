from django.db import models
import uuid

from jobs.models import Job


class Analytics(models.Model):
    analytics_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='analytics')
    views = models.PositiveIntegerField(default=0)
    applications = models.PositiveIntegerField(default=0)
    date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Analytics'
        ordering = ['-date']

    def __str__(self):
        return f"Analytics for {self.job.title} on {self.date}"
