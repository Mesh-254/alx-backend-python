from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import Conversation, Message

class IsParticipantOfConversation(BasePermission):
    """
    Custom permission to allow only participants in a conversation
    to send, view, update, and delete messages or conversations.
    """
    def has_object_permission(self, request, view, obj):
        # Allow read-only access for safe methods if the user is authenticated.
        if request.method in SAFE_METHODS and request.user.is_authenticated:
            return True

        # For Conversations, check if the user is a participant.
        if isinstance(obj, Conversation):
            return request.user in obj.participants.all()

        # For Messages, check if the user is the sender or part of the conversation.
        if isinstance(obj, Message):
            return (request.user == obj.sender or 
                    request.user in obj.conversation.participants.all())

        return False
