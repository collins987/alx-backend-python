from django.db import models

class UnreadMessagesManager(models.Manager):
    def unread_for_user(self, user):
        return self.filter(recipient=user, read=False).only('id', 'sender', 'content', 'timestamp').select_related('sender')
