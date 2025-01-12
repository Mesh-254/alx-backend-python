from .models import Message, Notification, MessageHistory
from django.contrib.auth.models import User
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.http import HttpResponse


def delete_user_account(request):
    """
    Function to delete a user account and all associated data.
    """
    user = request.user
    user.delete() # This will trigger the post_delete signal
    return HttpResponse("Your account has been deleted successfully.")



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