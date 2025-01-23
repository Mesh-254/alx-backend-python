from rest_framework import serializers
from .models import User, Conversation, Message


class UserSerializer(serializers.HyperlinkedModelSerializer):
    # This will calculate the full name dynamically.
    full_name = serializers.SerializerMethodField()

    # Password as a write-only field
    password = serializers.CharField(write_only=True, required=True, style={
                                     'input_type': 'password'})

    class Meta:
        model = User
        fields = ['user_id', 'first_name', 'last_name', 'email',
                  'phone_number', 'role', 'created_at', 'password', 'full_name']
        read_only_fields = ['user_id', 'created_at']

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
            raise serializers.ValidationError(
                "Emails from 'example.com' are not allowed.")
        return value

    def create(self, validated_data):
        """
        Create and return a new `CustomUser` instance, given the validated data.
        """
        # Use the create_user method for password hashing if it's implemented.
        password = validated_data.pop('password', None)
        user = User.objects.create(**validated_data)
        if password:
            user.set_password(password)  # Hash the password
        user.save()
        return user

    def update(self, instance, validated_data):
        """
        Update and return an existing `User` instance, given the validated data.
        """
        password = validated_data.pop('password', None)
        instance = super().update(instance, validated_data)
        if password:
            instance.set_password(password)  # Hash the password
            instance.save()
        return instance


class ConversationSerializer(serializers.HyperlinkedModelSerializer):
    messages = serializers.HyperlinkedIdentityField(
        view_name='messages-detail', many=True, read_only=True)  
    participants = serializers.HyperlinkedRelatedField(queryset=User.objects.all(), many=True, view_name='users-detail')

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'created_at', 'messages']

    def validate_participants_id(self, value):
        """
        Ensure that at least two participants are provided in the conversation.
        """
        if len(value) < 2:
            raise serializers.ValidationError(
                "A conversation must have at least two participants.")
        return value

    def create(self, validated_data):
        """
        Create and return a new `Conversation` instance, given the validated data.
        """
        # Remove participants from the data and create the conversation
        participants_data = validated_data.pop('participants')
        conversation = Conversation.objects.create(**validated_data)

        # Add participants to the conversation's ManyToMany field
        conversation.participants.set(participants_data)
        conversation.save()
        return conversation

    def update(self, instance, validated_data):
        """
        Update and return an existing `Conversation` instance, given the validated data.
        """
        participants_data = validated_data.pop('participants', None)
        instance = super().update(instance, validated_data)

        if participants_data is not None:
            # Update the participants if provided
            instance.participants.set(participants_data)

        instance.save()
        return instance


class MessageSerializer(serializers.HyperlinkedModelSerializer):
    sender = serializers.HyperlinkedRelatedField(view_name='users-detail', read_only=True)
    recipient = serializers.HyperlinkedRelatedField(view_name='users-detail', read_only=True)  
    conversation = serializers.HyperlinkedRelatedField(view_name='conversations-detail', read_only=True)  
    # Preview field changed to CharField.
    message_preview = serializers.CharField(read_only=True)

    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'conversation',
                  'message_body', 'sent_at', 'recipient', 'message_preview']

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
            raise serializers.ValidationError(
                "Message contains inappropriate language.")
        # Ensure the message isn't empty or only spaces.
        if len(value.strip()) == 0:
            raise serializers.ValidationError("Message body cannot be empty.")
        return value

    def validate(self, data):
        """Perform additional validation before saving the message."""
        conversation = data.get('conversation')
        if conversation:
            # Make sure you're filtering by `conversation_id`
            if not Conversation.objects.filter(conversation_id=conversation.conversation_id).exists():
                raise serializers.ValidationError("The conversation does not exist.")
        return data
