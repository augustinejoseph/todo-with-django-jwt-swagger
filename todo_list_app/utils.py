# utils.py (in one of your Django apps)

from celery import shared_task
from django.core.mail import EmailMessage
from django.conf import settings


@shared_task
def send_reminder_email(task_id):
    from .models import TodoTask  # Move the import here

    # Retrieve the task object using the task_id
    try:
        task = TodoTask.objects.get(pk=task_id)
    except TodoTask.DoesNotExist:
        # Handle the case where the task doesn't exist
        return

    subject = "Task Reminder"
    message = f"Don't forget to complete your task: {task.name} by {task.deadline}."
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [task.user.email]

    email = EmailMessage(subject, message, from_email, recipient_list)
    email.send()
