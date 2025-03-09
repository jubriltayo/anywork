from rest_framework import serializers
import hashlib

from .models import Resume


class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = '__all__'
        read_only_fields = ['resume_id', 'uploaded_at', 'checksum']

    def validate(self, data):
        # Calculate the checksum of the uploaded file
        file = data['file_path']
        sha256 = hashlib.sha256()
        for chunk in file.chunks():
            sha256.update(chunk)
        checksum = sha256.hexdigest()

        # Check if a resume with the same checksum already exists
        if Resume.objects.filter(checksum=checksum).exists():
            raise serializers.ValidationError("A resume with the same content already exists.")
        
        # Add the checksum to the validate data
        data['checksum'] = checksum
        return data
