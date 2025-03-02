from allauth.socialaccount.models import SocialAccount
from django.contrib.auth import get_user_model, authenticate
from django.db import IntegrityError
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
import requests

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


def authenticate_user_with_google(access_token):
    """
    Authenticate a user with Google OAuth
    """
    # Fetch user info from Google's API
    user_info_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(user_info_url, headers=headers)

    if response.status_code != 200:
        raise AuthenticationFailed("Invalid token or unable to fetch user info")

    user_info = response.json()

    try:
        # Check if a user with this email already exists
        user = User.objects.filter(email=user_info['email']).first()

        if not user:
            # Create a new user if one doesn't exist
            user = User.objects.create_user(email=user_info['email'])
            user.set_unusable_password()
            user.save()

        # Get or create the social account
        SocialAccount.objects.get_or_create(
            provider='google',
            uid=user_info['id'],
            defaults={'user': user}
        )

        return user
    except Exception:
        raise AuthenticationFailed("Invalid token or user not found")


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



