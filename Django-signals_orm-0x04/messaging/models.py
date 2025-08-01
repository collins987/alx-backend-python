from django.db import models
from django.contrib.auth.models import User
from messaging.models import Message
from .managers import UnreadMessagesManager
# Create your models here.
class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
    parent_message = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)
    read = models.BooleanField(default=False)
    objects = models.Manager()
    unread = UnreadMessagesManager()
    messages = Message.objects.filter(receiver=request.user)\
    .select_related('sender', 'receiver')\
    .prefetch_related('messagehistory_set')

# Recursive thread function

def get_thread(message):
    replies = Message.objects.filter(parent_message=message)
    return {
        "message": message,
        "replies": [get_thread(reply) for reply in replies]
    }

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

class MessageHistory(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)

class UnreadMessagesManager(models.Manager):
    def for_user(self, user):
        return self.filter(receiver=user, read=False).only('content', 'timestamp')
