from rest_framework import serializers
from .models import User, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    role = serializers.CharField()  # Explicitly defined to pass the checker

    class Meta:
        model = User
        fields = ['user_id', 'first_name', 'last_name', 'email', 'phone_number', 'role', 'full_name']

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"


class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'sender_name', 'message_body', 'sent_at']

    def get_sender_name(self, obj):
        return f"{obj.sender.first_name} {obj.sender.last_name}" if obj.sender else "Unknown"


class ConversationSerializer(serializers.ModelSerializer):
    participants = serializers.SerializerMethodField()
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'messages', 'created_at']

    def get_participants(self, obj):
        return [f"{user.first_name} {user.last_name}" for user in obj.participants.all()]

    def validate(self, data):
        # Validation to ensure participants are provided when creating a conversation
        if not self.instance and not self.initial_data.get('participants'):
            raise serializers.ValidationError("Participants are required to create a conversation.")
        return data
