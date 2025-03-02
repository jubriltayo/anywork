from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
import requests

from .models import User, JobSeeker, Employer
from .serializers import UserSerializer, JobSeekerSerializer, EmployerSerializer
from .auth import create_user, authenticate_user_with_google, generate_tokens_for_user, authenticate_user


# Authentication Views
class UserRegistrationView(APIView):
    """
    API endpoint to register users.
    """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save() # calls create_user internally
            return Response({
                "status": "success",
                "message": "User registered successfully",
                "data": {
                    "user": UserSerializer(user).data,
                }
            }, status=status.HTTP_201_CREATED)
        return Response({
            "status": "error",
            "message": "Invalid data",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """
    API endpoint to login users.
    """
    permission_classes = [AllowAny]

    def post (self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({
                "status": "error",
                "message": "Email and password are required"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = authenticate_user(email.lower(), password)
            tokens = generate_tokens_for_user(user)

            serializer = UserSerializer(user)
            
            return Response({
                "status": "success",
                "message": "Login successful",
                "data": {
                    **tokens,
                    "user": serializer.data
                }
            }, status=status.HTTP_200_OK)
        except AuthenticationFailed as e:
            return Response({
                "status": "error",
                "message": str(e)
            }, status=status.HTTP_401_UNAUTHORIZED)
        
"""
class GoogleLoginView(APIView):
    
    # API endpoint to handle Google OAuth login locally with no
    # client ID and client secret needed as google's default is used
    
    permission_classes = [AllowAny]

    def post(self, request):
        # Extract OAuth token from request 
        access_token = request.data.get('access_token')
        if not access_token:
            return Response({
                "status": "error",
                "message": "Access token is required"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = authenticate_user_with_google(request, access_token)
            tokens = generate_tokens_for_user(user)

            serializer = UserSerializer(user)
            return Response({
                "status": "success",
                "message": "Login Successful",
                "data": {
                    **tokens,
                    "user": serializer.data
                }
            }, status=status.HTTP_200_OK)
        except AuthenticationFailed as e:
            return Response({
                "status": "error",
                "message": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

"""

class GoogleLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # Get the authorization code from the frontend (retrieve manually for now)
        authorization_code = request.data.get('code')
        if not authorization_code:
            raise AuthenticationFailed("Authorization code is required")

        # Exchange authorization code for access token
        token_url = "https://oauth2.googleapis.com/token"
        payload = {
            'code': authorization_code,
            'client_id': settings.GOOGLE_OAUTH_CLIENT_ID,
            'client_secret': settings.GOOGLE_OAUTH_CLIENT_SECRET,
            'redirect_uri': settings.GOOGLE_OAUTH_REDIRECT_URI,
            'grant_type': 'authorization_code',
        }

        response = requests.post(token_url, data=payload)

        if response.status_code != 200:
            raise AuthenticationFailed("Failed to exchange authorization code for access token")

        # Extract the access token
        token_data = response.json()
        access_token = token_data.get('access_token')

        if not access_token:
            raise AuthenticationFailed("Access token not found in response")

        # Authenticate the user using the access token
        try:
            user = authenticate_user_with_google(access_token)
            tokens = generate_tokens_for_user(user)

            # Return the user and tokens
            return Response({
                "status": "success",
                "message": "Login successful",
                "data": {
                    **tokens,
                    "user": UserSerializer(user).data
                }
            })
        except Exception as e:
            raise AuthenticationFailed("Invalid token or user not found")


# API Views
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint to manage users.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        # Prevent creating users via this API
        return Response({
            "status": "error",
            "message": "User creation is not allowed via this endpoint. Please use the registration endpoint instead."
        }, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def list(self, request, *args, **kwargs):
        if request.user.role != 'admin':
            return Response({
                "status": "error",
                "message": "You do not have permission to view all users. Only admins can access this resource."
            }, status=status.HTTP_403_FORBIDDEN)
        return super().list(request, *args, **kwargs)

    @action(detail=False, methods=['delete'], url_path='delete-account')
    def delete_account(self, request, *args, **kwargs):
        user = request.user
        user.delete()
        return Response({
            "status": "success",
            "message": "Your account has been deleted successfully"
        }, status=status.HTTP_204_NO_CONTENT)


class JobSeekerViewSet(viewsets.ModelViewSet):
    """
    API endpoint to manage job seekers
    """
    queryset = JobSeeker.objects.all()
    serializer_class = JobSeekerSerializer
    permission_class = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        # Disable POST/create for JobSeeker
        return Response({
            "status": "error",
            "message": "JobSeeker profiles are created automatically during user registration. Use PUT/PATCH to update the profile."
        }, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def get_queryset(self):
        # Restrict users to only access their own profile
        if self.request.user.role == 'job_seeker':
            return JobSeeker.objects.filter(user=self.request.user)
        elif self.request.user.role == 'admin':
            return JobSeeker.objects.all()
        else:
            raise PermissionDenied("You do not have permission to access this resource.")


class EmployerViewSet(viewsets.ModelViewSet):
    queryset = Employer.objects.all()
    serializer_class = EmployerSerializer
    permission_class = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        # Disable POST/create for Employer
        return Response({
            "status": "error",
            "message": "Employer profiles are created automatically during user registration. Use PUT/PATCH to update the profile."
        }, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def get_queryset(self):
        # Restrict users to only access their own profile
        if self.request.user.role == 'employer':
            return Employer.objects.filter(user=self.request.user)
        elif self.request.user.role == 'admin':
            return Employer.objects.all()
        else:
            raise PermissionDenied("You do not have permission to access this resource.")
















