from rest_framework import serializers
from .models import User, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    # This will calculate the full name dynamically.
    full_name = serializers.SerializerMethodField()

    # Password as a write-only field
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})


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



class ConversationSerializer(serializers.ModelSerializer):
    participants_id = serializers.PrimaryKeyRelatedField(
        many=True, queryset=User.objects.all())

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants_id', 'created_at']

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
        return Conversation.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Conversation` instance, given the validated data.
        """
        instance.participants_id = validated_data.get(
            'participants_id', instance.participants_id)
        instance.created_at = validated_data.get(
            'created_at', instance.created_at)
        instance.save()
        return instance


class MessageSerializer(serializers.ModelSerializer):
    sender_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    conversation = serializers.PrimaryKeyRelatedField(
        queryset=Conversation.objects.all())
    # Preview field changed to CharField.
    message_preview = serializers.CharField(read_only=True)

    class Meta:
        model = Message
        fields = ['message_id', 'sender_id', 'conversation',
                  'message_body', 'sent_at', 'message_preview']

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
        """
        Perform additional validation before saving the message.
        """
        if data.get('conversation') and not Conversation.objects.filter(id=data['conversation'].id).exists():
            raise serializers.ValidationError(
                "The conversation does not exist.")
        return data
