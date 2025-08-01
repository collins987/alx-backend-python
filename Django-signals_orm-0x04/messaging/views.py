from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from .models import Message

@login_required
def delete_user(request):
    request.user.delete()
    return redirect('/')

@login_required
def inbox(request):
    # Use the custom unread manager and optimize the query
    unread_messages = Message.unread.unread_for_user(request.user).only('id', 'content', 'sender', 'timestamp')
    return render(request, 'messaging/inbox.html', {'unread_messages': unread_messages})

@login_required
def threaded_conversation(request, message_id):
    # Get root message with related sender and replies
    root_message = get_object_or_404(
        Message.objects.select_related('sender')
        .prefetch_related('replies__sender'), 
        id=message_id
    )

    # Recursive fetch of replies
    def fetch_replies(message):
        replies = message.replies.select_related('sender').prefetch_related('replies__sender').all()
        return [{'message': reply, 'replies': fetch_replies(reply)} for reply in replies]

    conversation = {'message': root_message, 'replies': fetch_replies(root_message)}
    return render(request, 'messaging/threaded.html', {'conversation': conversation})

@cache_page(60)
@login_required
def message_list(request):
    messages = (
        Message.objects
        .filter(receiver=request.user)
        .select_related('sender', 'receiver')
        .only('id', 'content', 'sender', 'receiver', 'timestamp')
    )
    return render(request, 'messaging/list.html', {'messages': messages})
