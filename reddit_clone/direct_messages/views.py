from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import JsonResponse

from .models import Conversation, Message
from .forms import MessageForm

User = get_user_model()


@login_required
def inbox(request):
    conversations = request.user.conversations.prefetch_related(
        "participants", "messages"
    ).exclude(deleted_by=request.user)

    conv_data = []
    for conv in conversations:
        conv_data.append({
            "conv": conv,
            "other": conv.get_other_participant(request.user),
            "last_msg": conv.get_last_message(),
            "unread": conv.unread_count_for(request.user),
        })

    return render(request, "direct_messages/inbox.html", {
        "conv_data": conv_data,
    })


@login_required
def conversation_detail(request, conversation_id):
    conversation = get_object_or_404(
        Conversation,
        pk=conversation_id,
        participants=request.user
    )
    other = conversation.get_other_participant(request.user)
    conversation.messages.filter(is_read=False).exclude(sender=request.user).update(is_read=True)

    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.conversation = conversation
            msg.sender = request.user
            msg.save()
            conversation.save()
            return redirect("dm:detail", conversation_id=conversation.pk)
    else:
        form = MessageForm()

    return render(request, "direct_messages/conversation_detail.html", {
        "conversation": conversation,
        "other": other,
        "chat_messages": conversation.messages.select_related("sender").exclude(deleted_by=request.user).order_by("created_at"),
        "form": form,
    })


@login_required
def delete_conversation(request, conversation_id):
    conversation = get_object_or_404(
        Conversation,
        pk=conversation_id,
        participants=request.user
    )

    if request.method == "POST":
        delete_for = request.POST.get("delete_for")

        if delete_for == "me":
            conversation.deleted_by.add(request.user)

        elif delete_for == "everyone":
            conversation.delete()

        return redirect("dm:inbox")

    other = conversation.get_other_participant(request.user)
    return render(request, "direct_messages/delete_confirm.html", {
        "conversation": conversation,
        "other": other,
    })


@login_required
def delete_message(request, message_id):
    message = get_object_or_404(
        Message,
        pk=message_id,
        conversation__participants=request.user
    )

    if request.method == "POST":
        delete_for = request.POST.get("delete_for")

        if delete_for == "me":
            message.deleted_by.add(request.user)

        elif delete_for == "everyone" and message.sender == request.user:
            message.delete()

        return redirect("dm:detail", conversation_id=message.conversation.pk)

    return render(request, "direct_messages/delete_message_confirm.html", {
        "message": message,
    })


@login_required
def new_conversation(request, username):
    other_user = get_object_or_404(User, username=username)

    if other_user == request.user:
        return redirect("dm:inbox")

    existing = Conversation.objects.filter(
        participants=request.user
    ).filter(
        participants=other_user
    ).first()

    if existing:
        return redirect("dm:detail", conversation_id=existing.pk)

    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            conv = Conversation.objects.create()
            conv.participants.add(request.user, other_user)
            msg = form.save(commit=False)
            msg.conversation = conv
            msg.sender = request.user
            msg.save()
            return redirect("dm:detail", conversation_id=conv.pk)
    else:
        form = MessageForm()

    return render(request, "direct_messages/new_conversation.html", {
        "other": other_user,
        "form": form,
    })


@login_required
def user_search(request):
    query = request.GET.get("q", "").strip()
    if len(query) < 2:
        return JsonResponse({"users": []})

    users = User.objects.filter(
        username__icontains=query
    ).exclude(
        pk=request.user.pk
    ).values("username")[:6]

    return JsonResponse({"users": list(users)})