from rest_framework import viewsets
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action


# ViewSet for listing conversations and creating a new conversation
class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]  # You might want to restrict this to authenticated users.

    def create(self, request, *args, **kwargs):
        """
        Create a new conversation.
        """
        # The serializer expects data for participants and created_at
        # We can validate and create participants when needed
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


# ViewSet for listing messages and sending messages to an existing conversation
class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]  # Only allow authenticated users to send messages.

    def perform_create(self, serializer):
        """
        Override this method to add the 'sender' dynamically, based on the authenticated user.
        """
        serializer.save(sender=self.request.user)  # Assign sender as the current logged-in user.

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
            serializer.save(sender=request.user, conversation=conversation)  # Add conversation here
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
            serializer.save(sender=request.user, conversation=conversation)  # Ensure the conversation is associated
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

