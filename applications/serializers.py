from rest_framework import serializers

from .models import Application



class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = '__all__'
        read_only_fields = ['application_id', 'applied_at']