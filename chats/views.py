from rest_framework import viewsets, filters, permissions
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Enable searching by participant username or email
    filter_backends = [filters.SearchFilter]
    search_fields = ['participants__username', 'participants__email']

    def perform_create(self, serializer):
        # Automatically add the request user to the conversation participants
        conversation = serializer.save()
        conversation.participants.add(self.request.user)

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Enable ordering messages by sent timestamp
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['sent_at']
    ordering = ['sent_at']  # Default ordering

    def get_queryset(self):
        conversation_id = self.kwargs.get('conversation_pk')
        if conversation_id:
            return Message.objects.filter(conversation__conversation_id=conversation_id)
        return Message.objects.all()

    def perform_create(self, serializer):
        conversation_id = self.kwargs.get('conversation_pk')
        if conversation_id:
            conversation = Conversation.objects.get(conversation_id=conversation_id)
            serializer.save(sender=self.request.user, conversation=conversation)
        else:
            serializer.save(sender=self.request.user)
