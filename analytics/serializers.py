from rest_framework import serializers

from .models import Analytics



class AnalyticsSerializer(serializers.ModelSerializer):
    date = serializers.DateField(read_only=True)

    class Meta:
        model = Analytics
        fields = '__all__'