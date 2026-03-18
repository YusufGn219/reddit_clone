from django.db import models
from django.conf import settings
from communities.models import Community
from django.db.models import Sum

class Post(models.Model):
    community = models.ForeignKey (
        Community,
        on_delete=models.CASCADE,
        related_name="posts"
    )
    author = models.ForeignKey (
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="posts"
    )
    title = models.CharField(max_length=255)
    body = models.TextField(blank = True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    is_edited = models.BooleanField(default=False)

    class PostType(models.TextChoices):
        TEXT = "text", "Metin"
        IMAGE = "image", "Resim"
        LINK = "link", "Link"
    
    post_type = models.CharField(max_length=10, choices=PostType.choices, default=PostType.TEXT)
    image = models.ImageField(upload_to="posts/", blank=True, null=True)
    url = models.URLField(blank=True)
    
    def __str__(self):
        return f"{self.title} - {self.author.username}"

class Comment(models.Model):
    post = models.ForeignKey("posts.Post", on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments")

    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="children",
    )

    body = models.TextField(max_length=3000)
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    is_edited = models.BooleanField(default=False)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"Comment({self.id})"

    @property
    def score(self):
        return self.votes.aggregate(s=Sum("value"))["s"] or 0

class SavedPost(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE,
        related_name="saved_posts"
    )

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="saved_by"
    )
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "post")

    def __str__(self):
        return f"{self.user.username} saved {self.post.title}"
    

class Award(models.Model):
    GOLD = "gold"
    SILVER = "silver"
    BRONZE = "bronze"
    FUNNY = "funny"
    HELPFUL ="helpful"
    HOT = "hot"

    AWARD_CHOICES = [
        (GOLD,    "🥇 Gold"),
        (SILVER,  "🥈 Silver"),
        (BRONZE,  "🥉 Bronze"),
        (FUNNY,   "😂 Funny"),
        (HELPFUL, "🙏 Helpful"),
        (HOT,     "🔥 Hot"),
    ]

    ICONS = {
        GOLD:    "🥇",
        SILVER:  "🥈",
        BRONZE:  "🥉",
        FUNNY:   "😂",
        HELPFUL: "🙏",
        HOT:     "🔥",
    }

    giver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="given_awards"
    )    
    award_type = models.CharField(max_length = 20, choices = AWARD_CHOICES)
    post = models.ForeignKey(
        "Post",
        on_delete=models.CASCADE,
        related_name="awards",
        null = True,
        blank =True
    )
    comment = models.ForeignKey(
        "Comment",
        on_delete=models.CASCADE,
        related_name="awards",
        null = True,
        blank =True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["giver", "post"],
                condition=models.Q(post__isnull=False),
                name="unique_post_award"
            ),
            models.UniqueConstraint(
                fields=["giver", "comment"],
                condition=models.Q(comment__isnull=False),
                name="unique_comment_award"
            ),
        ]

    def __str__(self):
        return f"{self.get_award_type_display()} by {self.giver}"