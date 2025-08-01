from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.views.decorators.cache import cache_page
from messaging.models import Message
# Create your views here.

@login_required
def delete_user(request):
    request.user.delete()
    return redirect('/')
    unread_messages = Message.unread.for_user(request.user)

@cache_page(60)
def message_list(request):
    messages = Message.objects.filter(receiver=request.user)
    return render(request, 'messages/list.html', {'messages': messages})