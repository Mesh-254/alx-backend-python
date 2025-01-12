from ..Models import Message, MessageHistory
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.contrib.auth.models import User


@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    """
    Signal to log the message history whenever a message is edited.
    """
    if instance.pk:  # Ensure this is an update, not a new creation
        # Retrieve the current message content from the database
        old_message = Message.objects.get(pk=instance.pk)
        if old_message.content != instance.content:
            # if original message is is different from new message 
            # Log the old content in MessageHistory
            MessageHistory.objects.create(
                message=old_message,
                old_content= old_message.content,
            )
            # Update the edited flag in the original message
            instance.edited = True
            # Save the original message to MessageHistory
            old_message.save()

def message_history(message_id):
    """
    Display the message edit history in the user interface, 
    allowing users to view previous versions of their messages.

    """
    # Get the message history for a message
    message_history = MessageHistory.objects.filter(pk=message_id
    ).order_by('timestamp').all()
    return message_history
