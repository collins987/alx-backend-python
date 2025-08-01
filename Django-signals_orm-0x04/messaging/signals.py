from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message, Notification
from django.db.models.signals import pre_save
from .models import Message, Notification, MessageHistory

@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if instance.pk:
        old_message = Message.objects.get(pk=instance.pk)
        if old_message.content != instance.content:
            MessageHistory.objects.create(message=instance, old_content=old_message.content)
            instance.edited = True
            instance.save()

@receiver(post_save, sender=Message)
def notify_receiver(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(user=instance.receiver, message=instance)


@receiver(post_delete, sender=User)
def clean_user_data(sender, instance, **kwargs):
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()
    Notification.objects.filter(user=instance).delete()
    MessageHistory.objects.filter(message__sender=instance).delete()