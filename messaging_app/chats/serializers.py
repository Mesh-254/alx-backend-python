from rest_framework import viewsets
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
import django_filters


# Conversation Filter class to filter by participant
class ConversationFilter(django_filters.FilterSet):
    participants_id = django_filters.UUIDFilter(
        field_name="participants__user_id", lookup_expr='exact')

    class Meta:
        model = Conversation
        fields = ['participants_id']


# ViewSet for listing conversations and creating a new conversation
class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]  # Restrict to authenticated users
    filters = (DjangoFilterBackend,)
    filterset_class = ConversationFilter  # Attach custom filter

    def create(self, request, *args, **kwargs):
        """
        Create a new conversation.
        """
        # The serializer expects data for participants and created_at
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Save the new conversation and handle participants separately if needed
            conversation = serializer.save()

            # Add participants, if participants are included in the request, but not required
            participants = request.data.get("participants_id", [])
            conversation.participants.set(participants)
            conversation.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Message Filter class to filter by sender or conversation
class MessageFilter(django_filters.FilterSet):
    sender_id = django_filters.UUIDFilter(
        field_name="sender__user_id", lookup_expr='exact')
    conversation_id = django_filters.UUIDFilter(
        field_name="conversation__conversation_id", lookup_expr='exact')

    class Meta:
        model = Message
        fields = ['sender_id', 'conversation_id']


# ViewSet for listing messages and sending messages to an existing conversation
class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    # Only allow authenticated users to send messages.
    permission_classes = [IsAuthenticated]
    filters = (DjangoFilterBackend,)
    filterset_class = MessageFilter  # Attach custom filter

    def perform_create(self, serializer):
        """
        Override this method to add the 'sender' dynamically, based on the authenticated user.
        """
        serializer.save(
            # Assign sender as the current logged-in user.
            sender=self.request.user)

    def create(self, request, *args, **kwargs):
        """
        Send a message to a specific conversation.
        Instead of using request.data alone, we also need the conversation ID
        to relate the message to the correct conversation.
        """
        conversation_id = kwargs.get('conversation_id')
        conversation = get_object_or_404(Conversation, pk=conversation_id)

        # Adding the 'conversation' relationship before saving the message
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Add conversation here
            serializer.save(sender=request.user, conversation=conversation)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Optional: Custom action to handle sending messages
    @action(detail=True, methods=['post'], url_path='send-message')
    def send_message(self, request, pk=None):
        """
        This custom action allows sending a message to a conversation.
        It is an additional endpoint specifically for sending messages
        to a conversation without changing the normal create behavior.
        """
        conversation = get_object_or_404(Conversation, pk=pk)
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Ensure the conversation is associated
            serializer.save(sender=request.user, conversation=conversation)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
