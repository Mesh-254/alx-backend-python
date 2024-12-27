from rest_framework.permissions import BasePermission
from .models import Conversation, Message


class IsParticipantOrReadOnly(BasePermission):
    """
    Custom permission to allow access to Conversations only if the user is a participant.
    """

    def has_object_permission(self, request, view, obj):
        # Check if the user is part of the conversation participants.
        if isinstance(obj, Conversation):
            return request.user in obj.participants.all()
        return False


class IsSenderOrParticipant(BasePermission):
    """
    Custom permission to allow access to Messages only if the user is the sender or
    a participant in the conversation.
    """

    def has_object_permission(self, request, view, obj):
        # Check if the object is a Message.
        if isinstance(obj, Message):
            return request.user == obj.sender or request.user in obj.conversation.participants.all()
        return False
