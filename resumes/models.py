from django.db import models
import uuid
import hashlib
import os

from users.models import JobSeeker
from .validators import validate_file_size, validate_file_extension


class Resume(models.Model):
    resume_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    job_seeker = models.ForeignKey(JobSeeker, on_delete=models.CASCADE, related_name='resumes')
    file_path = models.FileField(
        upload_to='resumes/',
        validators=[validate_file_size, validate_file_extension]    
    )
    checksum = models.CharField(max_length=64, unique=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Resumes'
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"Resume {self.resume_id} for {self.job_seeker}"
    
    def save(self, *args, **kwargs):
        # Calculate file's checksum before saving to avoid duplicate file upload
        if not self.checksum:
            self.checksum = self.calculate_checksum()
        super().save(*args, **kwargs)

    def calculate_checksum(self):
        # Calculate the SHA-256 checksum of the file
        sha256 = hashlib.sha256()
        for chunk in self.file_path.chunks():
            sha256.update(chunk)
        return sha256.hexdigest()

    def delete(self, *args, **kwargs):
        # Override delete method to also delete the physical file
        file_path = self.file_path.path
        super().delete(*args, **kwargs)
        self.delete_file(file_path)

    def delete_file(self, file_path):
        # Delete the physical file from storage
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f"Error deleting file {file_path}: {e}")
