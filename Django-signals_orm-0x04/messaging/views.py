from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from messaging.models import Message

@login_required
def delete_user(request):
    """
    Deletes the currently authenticated user and redirects to the home page.
    """
    request.user.delete()
    return redirect('/')

@login_required
def inbox(request):
    """
    Display unread messages using the custom unread manager.
    """
    # ✅ FIXED: Using unread_for_user() from Message.unread
    unread_messages = Message.unread.unread_for_user(request.user).only('sender', 'content', 'timestamp')
    return render(request, 'messaging/inbox.html', {'unread_messages': unread_messages})

@login_required
def threaded_conversation(request, message_id):
    """
    Fetch a threaded conversation starting from a specific message.
    Uses select_related and prefetch_related to optimize query performance.
    Also ensures message was sent by the current user.
    """
    root_message = get_object_or_404(
        Message.objects.select_related('sender').prefetch_related('replies'),
        id=message_id,
        sender=request.user  
    )

    def fetch_replies(msg):
        replies = msg.message_set.select_related('sender').prefetch_related('message_set').all()
        return [{'message': reply, 'replies': fetch_replies(reply)} for reply in replies]

    conversation = {'message': root_message, 'replies': fetch_replies(root_message)}

    return render(request, 'messaging/threaded.html', {'conversation': conversation})

@cache_page(60)
@login_required
def message_list(request):
    """
    Cached list of all received messages.
    """
    messages = Message.objects.filter(receiver=request.user).select_related('sender').only('sender', 'content', 'timestamp')
    return render(request, 'messaging/message_list.html', {'messages': messages})
