from django.db import models
from django.urls import reverse

# Create your models here.
class Professional(models.Model):
    OPTIONS = [
        ('Tutorship', 'Tutorship'),
        ('Transportation', 'Transportation'),
        ('Food', 'Food'),
        ('Cleaning', 'Cleaning')
    ]
    name                = models.CharField(max_length=128, null=False)
    email               = models.EmailField(null=False)
    phone_number        = models.CharField(max_length=20, null=False)
    address             = models.TextField(null=False)
    service             = models.CharField(max_length=64, choices=OPTIONS)
    years_of_experience = models.PositiveSmallIntegerField(null=False)
    qualification       = models.TextField(null=False)
    price               = models.CharField(max_length=16, null=False)

def get_absolute_url(self):
    return reverse("professionals:professional-detail", kwargs={"id": self.id})