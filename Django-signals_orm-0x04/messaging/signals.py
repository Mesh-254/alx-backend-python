# se Django signals (e.g., post_save) to trigger a notification when a new Message instance is created.

from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from .models import Message, Notification, MessageHistory
from django.contrib.auth.models import User


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


@receiver(post_delete, sender=User)
def delete_user_messages(sender, instance, **kwargs):
    """
    Signal to delete all messages, notifications, and message histories
    associated with a user when the user is deleted.
    """
    # Delete all messages sent by the user
    Message.objects.filter(sender=instance).delete()

    # Delete all messages received by the user (if the user is the receiver)
    Message.objects.filter(receiver=instance).delete()

    # Delete notifications for the user
    Notification.objects.filter(user=instance).delete()

    # Delete message histories where the user is the editor or the original message sender
    MessageHistory.objects.filter(edited_by=instance).delete()
    MessageHistory.objects.filter(message__sender=instance).delete()
