# se Django signals (e.g., post_save) to trigger a notification when a new Message instance is created.

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message, Notification


@receiver(post_save, sender=Message)
def message_notification(sender, instance, created, **kwargs):
    """
    Signal to create a notification for the receiver 
    whenever a new message is created.
    """
    if created:
        Notification.objects.create(
            user=instance.receiver,  # Notify the receiving user
            message=instance,
            notification_text=f"New message from {instance.sender.username}",
        )


@receiver(post_save, sender=Notification)
def save_notification(sender, instance, **kwargs):
    instance.save()
