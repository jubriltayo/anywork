from django.db import models
import uuid

from users.models import User


class Skill(models.Model):
    skill_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='skills')

    class Meta:
        verbose_name_plural = 'Skills'
        ordering = ['name']

    def __str__(self):
        return self.name
    