from .models import Message
from django.db import models
from flask import request


class UnreadMessagesManager(models.Manager):
    """
     custom manager that filters unread messages for a specific user.
    """

    def unread_for_user(self, user):
        """
        Returns a queryset of unread messages for the given user.
        """
        return self.filter(receiver=user, read=False)


