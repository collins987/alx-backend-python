import django_filters
from .models import Message

class MessageFilter(django_filters.FilterSet):
    timestamp = django_filters.DateFromToRangeFilter()

    class Meta:
        model = Message
        fields = ['sender', 'timestamp']
