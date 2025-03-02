from rest_framework import serializers
from .models import User
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

    # To ensure password hashing
    def create(self, validated_data):
        user = create_user(**validated_data)
        return user
    

# class LoginSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#     password = serializers.CharField(max_length=128, write_only=True)