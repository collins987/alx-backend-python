from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.views.decorators.cache import cache_page
from messaging.models import Message
from .models import Message
# Create your views here.

@login_required
def delete_user(request):
    request.user.delete()
    return redirect('/')
    unread_messages = Message.unread.for_user(request.user)

@login_required
def inbox(request):
    # Get unread messages using custom manager
    unread_messages = Message.unread.unread_for_user(request.user)

    return render(request, 'messaging/inbox.html', {'unread_messages': unread_messages})


@login_required
def threaded_conversation(request, message_id):
    # Get root message
    root_message = Message.objects.select_related('sender').get(id=message_id)

    # Recursive fetch (manually constructed)
    def fetch_replies(msg):
        replies = msg.replies.select_related('sender').all()
        return [{'message': reply, 'replies': fetch_replies(reply)} for reply in replies]

    conversation = {'message': root_message, 'replies': fetch_replies(root_message)}

    return render(request, 'messaging/threaded.html', {'conversation': conversation})
    
@cache_page(60)
def message_list(request):
    messages = Message.objects.filter(receiver=request.user)
    return render(request, 'messages/list.html', {'messages': messages})