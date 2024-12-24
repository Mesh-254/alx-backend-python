from rest_framework import serializers
from .models import User, Conversation, Message
from rest_framework.exceptions import ValidationError


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()  # This will calculate the full name dynamically.

    class Meta:
        model = User
        fields = ['user_id', 'first_name', 'last_name', 'email', 'phone_number', 'role', 'created_at', 'full_name']
    
    def get_full_name(self, obj):
        """
        Return the full name by combining first and last names.
        """
        return f"{obj.first_name} {obj.last_name}"

    def validate_email(self, value):
        """
        Custom validation for email field. Raise an error if email is from a non-permitted domain.
        """
        if '@example.com' in value:
            raise ValidationError("Emails from 'example.com' are not allowed.")
        return value

    def create(self, validated_data):
        """
        Create and return a new `User` instance, given the validated data.
        """
        return User.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `User` instance, given the validated data.
        """
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.role = validated_data.get('role', instance.role)
        instance.created_at = validated_data.get('created_at', instance.created_at)
        instance.save()
        return instance


class ConversationSerializer(serializers.ModelSerializer):
    participants_id = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants_id', 'created_at']
    
    def validate_participants_id(self, value):
        """
        Ensure that at least two participants are provided in the conversation.
        """
        if len(value) < 2:
            raise ValidationError("A conversation must have at least two participants.")
        return value

    def create(self, validated_data):
        """
        Create and return a new `Conversation` instance, given the validated data.
        """
        return Conversation.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Conversation` instance, given the validated data.
        """
        instance.participants_id = validated_data.get('participants_id', instance.participants_id)
        instance.created_at = validated_data.get('created_at', instance.created_at)
        instance.save()
        return instance


class MessageSerializer(serializers.ModelSerializer):
    sender_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    conversation = serializers.PrimaryKeyRelatedField(queryset=Conversation.objects.all())
    message_preview = serializers.SerializerMethodField()  # Custom field to show a preview of the message.

    class Meta:
        model = Message
        fields = ['message_id', 'sender_id', 'conversation', 'message_body', 'sent_at', 'message_preview']

    def get_message_preview(self, obj):
        """
        Generate a preview of the message by truncating the message body.
        """
        return obj.message_body[:30]  # Returns the first 30 characters as a preview.

    def validate_message_body(self, value):
        """
        Custom validation for message body, checking if it contains profanity.
        """
        if 'badword' in value.lower():
            raise ValidationError("Message contains inappropriate language.")
        return value

    def create(self, validated_data):
        """
        Create and return a new `Message` instance, given the validated data.
        """
        return Message.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Message` instance, given the validated data.
        """
        instance.sender_id = validated_data.get('sender_id', instance.sender_id)
        instance.conversation = validated_data.get('conversation', instance.conversation)
        instance.message_body = validated_data.get('message_body', instance.message_body)
        instance.sent_at = validated_data.get('sent_at', instance.sent_at)
        instance.save()
        return instance
