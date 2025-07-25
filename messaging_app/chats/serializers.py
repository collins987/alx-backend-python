from rest_framework import serializers
from .models import User, Conversation, Message

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'content', 'timestamp']

class ConversationSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'messages']

    def validate(self, data):
        if 'participants' not in data:
            raise serializers.ValidationError("Participants are required")
        return data
