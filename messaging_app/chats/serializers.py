from rest_framework import serializers
from models import User, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'first_name', 'last_name',
                  'email', 'phone_number', 'role', 'created_at']


class ConversationSerializer(serializers.ModelSerializer):
    
    participants_id= serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants_id', 'created_at']


class MessageSerializer(serializers.ModelSerializer):

    sender_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    conversation = serializers.PrimaryKeyRelatedField(queryset=Conversation.objects.all())
    
    class Meta:
        model = Message
        fields = ['message_id', 'sender_id', 'conversation',
                  'message_body', 'sent_at']