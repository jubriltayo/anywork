from rest_framework import serializers
from .models import User, JobSeeker, Employer
from .auth import create_user



class UserSerializer(serializers.ModelSerializer):
    """ 
    A singular serializer that handles user registration (with password hashed) and user data
    """
    password = serializers.CharField(write_only=True) # accepts plain password for registration

    class Meta:
        model = User
        fields = ['user_id', 'email', 'password', 'role', 'created_at', 'updated_at']
        read_only_fields = ['user_id', 'created_at', 'updated_at']

    def validate_role(self, value):
        # Ensure role is valid
        if value not in [role[0] for role in User.USER_ROLE]:
            raise serializers.ValidationError("Invalid role")
        return value
    
    def create(self, validated_data):
        user = create_user(**validated_data)
        return user
    

class JobSeekerSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobSeeker
        fields = ['user', 'first_name', 'last_name', 'phone_number']
        read_only_fields = ['user']



class EmployerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employer
        fields = ['user', 'company_name', 'company_description', 'website']
        read_only_fields = ['user']