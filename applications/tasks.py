from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def send_application_creation_email(recipient_email):
    # Send an application creation email asynchronously
    subject = "Successful Application"
    message = "Congratulations! Your application is successfully completed"
    # sender = settings.EMAIL_HOST_USER
    sender = 'noreply@anywork.com'

    recipient_list = [recipient_email]

    send_mail(subject, message, sender, recipient_list)


@shared_task
def send_application_status_change_notification(application_id):
    # Send an application status change email asynchronously
    from .models import Application

    try:
        application = Application.objects.get(pk=application_id)
        subject = f"Application Status Update: {application.job.title}"
        message = f"Your application for {application.job.title} has been {application.status}."
        # sender = settings.EMAIL_HOST_USER
        sender = 'noreply@anywork.com'
        
        recipient_list = [application.job_seeker.user.email]
        # Send email to the job seeker
        send_mail(subject, message, sender, recipient_list)

    except Application.DoesNotExist:
        pass
