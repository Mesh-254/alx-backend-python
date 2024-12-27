from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import User, Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsParticipantOrReadOnly, IsSenderOrParticipant


class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Conversations.
    """
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    permission_classes = [IsAuthenticated, IsParticipantOrReadOnly]

    def get_queryset(self):
        if isinstance(self.request.user, User):  # Check if the user is a valid instance of the custom User model
            return Conversation.objects.filter(participants=self.request.user)
        return Conversation.objects.none()  # Return no results for invalid user instances


class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Messages.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['sent_at']
    ordering = ['-sent_at']
    permission_classes = [IsAuthenticated, IsSenderOrParticipant]

    def get_queryset(self):
        if isinstance(self.request.user, User):  # Check if the user is a valid instance of the custom User model
            return Message.objects.filter(conversation__participants=self.request.user)
        return Message.objects.none()  # Return no results for invalid user instances
