"""
Context processors for accounts app
"""
from .models import Message


def unread_messages_count(request):
    """
    Add unread message count to all template contexts
    """
    if request.user.is_authenticated:
        unread_count = Message.objects.filter(
            recipient=request.user,
            is_read=False
        ).count()
        return {'unread_messages_count': unread_count}
    return {'unread_messages_count': 0}

