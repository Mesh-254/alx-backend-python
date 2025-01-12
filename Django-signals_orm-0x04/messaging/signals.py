# se Django signals (e.g., post_save) to trigger a notification when a new Message instance is created.

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Message, Notification, MessageHistory


@receiver(post_save, sender=Message)
def message_notification(sender, instance, created, **kwargs):
    """
    Signal to create a notification for the receiver 
    whenever a new message is created.
    """
    if created:
        Notification.objects.create(
            user=instance.receiver,  # Notify the receiving user
            message=instance,  # Pass the entire Message instance
            notification_text=f"New message from {instance.sender.username}",
        )


@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    """
    Signal to log the message history whenever a message is edited.
    """
    if instance.pk:  # Ensure this is an update, not a new creation
        # Retrieve the current message content from the database
        original_message = Message.objects.get(pk=instance.pk)
        if original_message.content != instance.content:
            # if original message is is different from new message
            # Log the old content in MessageHistory
            MessageHistory.objects.create(
                message=original_message,
                old_content=original_message.content,
            )
            # Update the edited flag in the instance being saved
            instance.edited = True


def message_history(message_id):
    """
    Display the message edit history in the user interface, 
    allowing users to view previous versions of their messages.

    """
    # Get the message history for a message
    message_history = MessageHistory.objects.filter(pk=message_id
                                                    ).order_by('timestamp').all()
    return message_history
