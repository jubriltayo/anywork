from django.contrib.auth import get_user_model, authenticate
from django.db import IntegrityError
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken

from .models import JobSeeker, Employer

User = get_user_model()


def create_user(email, password, role, **extra_fields):
    """
    Create a new user and their role specific profile (JobSeeker or Employer)
    """
    if role not in [role[0] for role in User.USER_ROLE]:
        raise ValidationError({"error": "Invalid role"})
    
    try:
        user = User.objects.create_user(email=email, password=password, role=role, **extra_fields)
        
        if role == 'job_seeker':
            JobSeeker.objects.create(user=user, **extra_fields)
        elif role == 'employer':
            Employer.objects.create(user=user, **extra_fields)
        
        return user
    except IntegrityError:
        raise ValidationError({"error": "A user with this email already exists."})
    except Exception as e:
        raise ValidationError({"error": str(e)})


def generate_tokens_for_user(user):
    """
    Utility function to generate tokens for a user
    """
    try:
        token = RefreshToken.for_user(user)
        return {
            "accessToken": str(token.access_token),
            "refreshToken": str(token)
        }
    except Exception as e:
        raise ValidationError({"error": f"Failed to generate tokens: {str(e)}"})


def authenticate_user(email, password):
    """
    Standard function to authenticate a user
    """
    user = authenticate(email=email, password=password)
    if user is None:
        raise AuthenticationFailed("Invalid credentials")
    if not user.is_active:
        raise AuthenticationFailed("User is inactive")
    return user
