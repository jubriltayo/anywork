from django.contrib.auth.models import BaseUserManager
from django.core.validators import validate_email



class UserManager(BaseUserManager):
    def email_validator(self, email):
        try:
            validate_email(email)
        except:
            raise ValueError("Please enter a valid email address")

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("An email address is required")
            
        email = self.normalize_email(email)
        self.email_validator(email)
        
        extra_fields.setdefault("is_active", True)
        
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, password, **extra_fields)
