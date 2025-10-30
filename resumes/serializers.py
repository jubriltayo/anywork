from rest_framework import serializers
import hashlib

from .models import Resume


class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = ['resume_id', 'file_path', 'checksum', 'uploaded_at', 'job_seeker']
        read_only_fields = ['resume_id', 'uploaded_at', 'checksum', 'job_seeker']

    def validate(self, data):
        # Check if file_path exists in the data
        if 'file_path' not in data:
            raise serializers.ValidationError("File is required.")
        
        file = data['file_path']
        
        # Calculate the checksum of the uploaded file
        sha256 = hashlib.sha256()
        for chunk in file.chunks():
            sha256.update(chunk)
        checksum = sha256.hexdigest()

        # Check if a resume with the same checksum already exists for this job seeker
        if self.context['request'].user.role == 'job_seeker':
            job_seeker = self.context['request'].user.job_seeker
            if Resume.objects.filter(checksum=checksum, job_seeker=job_seeker).exists():
                raise serializers.ValidationError("You have already uploaded a resume with the same content.")
        
        # Add the checksum to the validated data
        data['checksum'] = checksum
        return data