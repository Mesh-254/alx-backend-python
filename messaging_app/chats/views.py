from rest_framework.response import Response
from rest_framework import viewsets, status
from django_filters.rest_framework import DjangoFilterBackend
from .models import User, Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsParticipantOfConversation
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import OrderingFilter

class CustomUserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Users.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Conversations.
    """
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        # Ensure users only see conversations they participate in.
        return Conversation.objects.filter(participants=self.request.user)

# Custom pagination class


class MessagePagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Messages.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ['sent_at']
    ordering = ['-sent_at']

    def get_queryset(self):
        # Ensure users only see messages related to their conversations.
        return Message.objects.filter(conversation__participants=self.request.user)

    