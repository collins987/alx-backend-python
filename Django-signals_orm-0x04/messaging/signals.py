from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Message, Notification, MessageHistory


@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_message = Message.objects.get(pk=instance.pk)
            if old_message.content != instance.content:
                # Track who edited the message
                edited_by = instance.sender  # Assume sender is the editor (you can customize this logic)

                MessageHistory.objects.create(
                    message=instance,
                    old_content=old_message.content,
                    edited_by=edited_by  # New field
                )
                instance.edited = True  # Mark the message as edited
        except Message.DoesNotExist:
            pass  # New message, no edit history needed


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
