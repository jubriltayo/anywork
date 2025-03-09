from django.db import models
import uuid

from users.models import JobSeeker
from jobs.models import Job
from resumes.models import Resume
from notifications.models import Notification
from .tasks import send_application_status_change_notification



class Application(models.Model):
    APPLICATION_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('reviewed', 'Reviewed'),
        ('rejected', 'Rejected'),
        ('accepted', 'Accepted'),
    ]

    application_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    job_seeker = models.ForeignKey(JobSeeker, on_delete=models.CASCADE, related_name='applications')
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='applications')
    cover_letter = models.TextField()
    status = models.CharField(max_length=20, choices=APPLICATION_STATUS_CHOICES, default='pending')
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Applications'
        ordering = ['-applied_at']

    def save(self, *args, **kwargs):
        # Fetch the old status before saving (if application exists)
        old_status = None
        if self.pk:
            try:
                old_status = Application.objects.get(pk=self.pk).status
            except Application.DoesNotExist:
                pass

        # save the application
        super().save(*args, **kwargs)

        # Check if status has changed
        if old_status is not None and old_status != self.status:
            # Create a notification for the job seeker
            Notification.objects.create(
                user=self.job_seeker.user,
                message=f"Your application for {self.job.title} has been {self.status}"
            )

            # Trigger task to send an email notification
            send_application_status_change_notification(self.application_id)

    def __str__(self):
        return f"Application {self.application_id} for {self.job}"
