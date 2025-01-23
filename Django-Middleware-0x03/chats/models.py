from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLE_CHOICES = [
        ('guest', 'Guest'),
        ('host', 'Host'),
        ('admin', 'Admin'),
    ]

    user_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    first_name = models.CharField(max_length=50, null=False)
    last_name = models.CharField(max_length=50, null=False)
    email = models.EmailField(unique=True, null=False)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    role = models.CharField(
        max_length=10, choices=ROLE_CHOICES, null=False, default='guest')
    password = models.CharField(max_length=128, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name',
                       'last_name', 'phone_number', 'role']

    class Meta:
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['user_id']),
        ]

    def __str__(self):
        return f"{self.email} - {self.first_name} {self.last_name} . {self.role}"


class Conversation(models.Model):
    conversation_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    participants = models.ManyToManyField(User, related_name="conversations")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['conversation_id']),
        ]

    def __str__(self):
        return f"{self.conversation_id}"


class Message(models.Model):
    message_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sent_messages")
    conversation = models.ForeignKey(
        Conversation, on_delete=models.CASCADE, related_name="messages", null=True, default=None)
    recipient = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="received_messages"
    )
    message_body = models.TextField(null=False)
    sent_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['message_id']),
            models.Index(fields=['sender']),
            models.Index(fields=['recipient'])
        ]

    def __str__(self):
        return f"Message {self.message_id} from {self.sender.email} to {self.recipient.email}"
