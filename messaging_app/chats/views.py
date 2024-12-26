from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import User, Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Conversations.
    """
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['participants', 'created_at']  # Filter conversations by participants
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def create(self, request, *args, **kwargs):
        """
        Create a new conversation.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Messages.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    # Filter by conversation or sender
    filterset_fields = ['conversation', 'sender']
    ordering_fields = ['sent_at']
    ordering = ['-sent_at']

    def create(self, request, *args, **kwargs):
        """
        Send a message in an existing conversation.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        """
        Perform additional actions on creating a message.
        """
        serializer.save()


class ConversationFilter(filters.FilterSet):
    """
    FilterSet for filtering Conversations.
    """
    participants = filters.CharFilter(field_name="participants__username", lookup_expr="icontains")

    class Meta:
        model = Conversation
        fields = ['participants']


class MessageFilter(filters.FilterSet):
    """
    FilterSet for filtering Messages.
    """
    conversation = filters.NumberFilter(field_name="conversation__id")
    sender = filters.CharFilter(field_name="sender__username", lookup_expr="icontains")
    

    class Meta:
        model = Message
        fields = ['conversation', 'sender']