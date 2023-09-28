# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import TodoTask
from .utils import send_reminder_email


@receiver(post_save, sender=TodoTask)
def schedule_task_reminder(sender, instance, **kwargs):
    if instance.deadline > timezone.now():
        reminder_time = instance.deadline - timezone.timedelta(hours=1)

        send_reminder_email.apply_async(args=[instance.pk], eta=reminder_time)
