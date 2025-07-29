from rest_framework import viewsets, filters, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['participants__username', 'participants__email']

    def perform_create(self, serializer):
        conversation = serializer.save()
        conversation.participants.add(self.request.user)

    @action(detail=True, methods=['get', 'post'], permission_classes=[permissions.IsAuthenticated])
    def messages(self, request, pk=None):
        conversation = self.get_object()

        if request.method == 'GET':
            messages = conversation.messages.order_by('sent_at')
            serializer = MessageSerializer(messages, many=True)
            return Response(serializer.data)

        elif request.method == 'POST':
            serializer = MessageSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(sender=request.user, conversation=conversation)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['sent_at']
    ordering = ['sent_at']

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)
