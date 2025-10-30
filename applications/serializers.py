from rest_framework import serializers
from .models import Application
from users.models import JobSeeker
from resumes.models import Resume

class ApplicationSerializer(serializers.ModelSerializer):
    # Include nested job seeker details
    job_seeker_details = serializers.SerializerMethodField()
    
    # Include nested resume details
    resume_details = serializers.SerializerMethodField()
    
    class Meta:
        model = Application
        fields = [
            'application_id', 
            'job_seeker', 
            'job_seeker_details',
            'job', 
            'resume', 
            'resume_details',
            'cover_letter', 
            'status', 
            'applied_at'
        ]
        read_only_fields = ['application_id', 'applied_at']

    def get_job_seeker_details(self, obj):
        """Get job seeker details for the application"""
        job_seeker = obj.job_seeker
        return {
            'first_name': job_seeker.first_name,
            'last_name': job_seeker.last_name,
            'full_name': f"{job_seeker.first_name} {job_seeker.last_name}",
            'phone_number': job_seeker.phone_number,
            'email': job_seeker.user.email
        }

    def get_resume_details(self, obj):
        """Get resume details for the application"""
        resume = obj.resume
        if resume and resume.file_path:
            # Build absolute URL for the file
            file_url = self.context['request'].build_absolute_uri(resume.file_path.url)
            return {
                'resume_id': resume.resume_id,
                'file_url': file_url,
                'file_name': resume.file_path.name.split('/')[-1],
                'uploaded_at': resume.uploaded_at
            }
        return None
