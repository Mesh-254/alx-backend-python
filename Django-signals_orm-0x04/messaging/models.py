from django.db import models
from django.contrib.auth.models import User


class Message(models.Model):
    """
    Model representing a message sent between users.
    """
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='sent_messages',
        help_text="User who sent the message."
    )
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='received_messages',
        help_text="User who will receive the message."
    )
    content = models.TextField(
        max_length=1000, help_text="Content of the message."
    )
    created_at = models.DateTimeField(
        auto_now_add=True, help_text="Timestamp when the message was created."
    )

    def __str__(self):
        return f'{self.sender.username} -> {self.receiver.username}: {self.content[:20]}'


class Notification(models.Model):
    """
    Model representing a notification for a user.
    """
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='notifications',
        help_text="User for whom the notification is created."
    )
    message = models.ForeignKey(
        Message, on_delete=models.CASCADE, related_name='notifications',
        help_text="Message associated with this notification."
    )
    notification_text = models.CharField(
        max_length=255, help_text="Details about the notification."
    )
    is_read = models.BooleanField(
        default=False, help_text="Whether the notification has been read by the user."
    )
    timestamp = models.DateTimeField(
        auto_now_add=True, help_text="Timestamp when the notification was created."
    )

    def __str__(self):
        return f"Notification for {self.user.username}: {self.notification_text}"
