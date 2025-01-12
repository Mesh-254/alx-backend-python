from .models import Message
from django.db import models
from flask import request


class UnreadMessagesManager(models.Manager):
    """
     custom manager that filters unread messages for a specific user.
    """

    def get_unread_messages(self, user):
        """
        Returns a queryset of unread messages for the given user.
        """
        return self.filter(receiver=user, read=False).only('id', 'sender', 'content', 'created_at')


