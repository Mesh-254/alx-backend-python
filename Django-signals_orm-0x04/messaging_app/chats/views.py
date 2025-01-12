from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from .models import User, Conversation, Message
from django.contrib.auth.models import User
from .serializers import ConversationSerializer, MessageSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsParticipantOfConversation
from rest_framework.pagination import PageNumberPagination
from django_filters import rest_framework as filters
from django.views.decorators.cache import cache_page


@cache_page(60) 
class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Conversations.
    """
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
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

# Filter for messages
class MessageFilter(filters.FilterSet):
    sender = filters.CharFilter(field_name="sender__username", lookup_expr="icontains")
    conversation = filters.NumberFilter(field_name="conversation__id")
    sent_before = filters.DateTimeFilter(field_name="sent_at", lookup_expr="lte")
    sent_after = filters.DateTimeFilter(field_name="sent_at", lookup_expr="gte")

    class Meta:
        model = Message
        fields = ['sender', 'conversation', 'sent_before', 'sent_after']

@cache_page(60) 
class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Messages.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = MessageFilter
    ordering_fields = ['sent_at']
    ordering = ['-sent_at']

    def get_queryset(self):
        # Ensure users only see messages related to their conversations.
        return Message.objects.filter(conversation__participants=self.request.user)