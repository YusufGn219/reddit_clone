from django.conf import settings
from django.db import models

class Conversation(models.Model):
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="conversations"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_by = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="deleted_conservations",
        blank=True,
    )
    
    class Meta:
        ordering = ["-updated_at"]
    
    def get_other_participant(self, user):
        return self.participants.exclude(pk = user.pk).first()
    
    def get_last_message(self):
        return self.messages.order_by("-created_at").first()

    def unread_count_for(self,user):
        return self.messages.filter(is_read=False).exclude(sender=user).count()

    def __str__(self):
        return f"Conversation #{self.pk}"


class Message(models.Model):
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name="messages"
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sent_messages"
    )
    deleted_by= models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="deleted_messages",
        blank=True,
    )
    body = models.TextField(max_length=2000)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
    
    def __str__(self):
         return f"Message from {self.sender} in Conversation #{self.conversation_id}"