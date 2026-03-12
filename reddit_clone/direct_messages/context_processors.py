from .models import Message


def unread_dm_count(request):
    if request.user.is_authenticated:
        count = Message.objects.filter(
            conversation__participants=request.user,
            is_read=False,
        ).exclude(sender=request.user).count()
        return {"unread_dm_count": count}
    return {"unread_dm_count": 0}