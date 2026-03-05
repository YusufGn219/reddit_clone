from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

from communities.models import Community
from posts.models import Post, Comment
from votes.models import PostVote, CommentVote
from votes.services import toggle_post_vote, toggle_comment_vote

User = get_user_model()

def make_user(username, password="pass"):
    return User.objects.create_user(username, password=password)

def make_community(user, name="testcomm"):
    return Community.objects.create(name=name, title="T", description="d", created_by=user)

def make_post(user, community):
    return Post.objects.create(title="Test Post", body="body", author=user, community=community)

def make_comment(user, post):
    return Comment.objects.create(body="A comment", author=user, post=post)

class TogglePostVoteTest(TestCase):

    def setUp(self):
        self.user = make_user("voter")
        self.community = make_community(self.user)
        self.post = make_post(self.user, self.community)

    def test_upvote_creates_vote(self):
        toggle_post_vote(post=self.post, user=self.user, value=1)
        self.assertEqual(PostVote.objects.filter(post=self.post, user=self.user, value=1).count(), 1)

    def test_same_upvote_again_removes_vote(self):
        toggle_post_vote(post=self.post, user=self.user, value=1)
        toggle_post_vote(post=self.post, user=self.user, value=1)
        self.assertEqual(PostVote.objects.filter(post=self.post, user=self.user).count(), 0)

    def test_upvote_to_downvote_changes_value(self):
        toggle_post_vote(post=self.post, user=self.user, value=1)
        toggle_post_vote(post=self.post, user=self.user, value=-1)
        vote = PostVote.objects.get(post=self.post, user=self.user)
        self.assertEqual(vote.value, -1)

    def test_downvote_creates_vote(self):
        toggle_post_vote(post=self.post, user=self.user, value=-1)
        self.assertEqual(PostVote.objects.filter(post=self.post, user=self.user, value=-1).count(), 1)

    def test_same_downvote_again_removes_vote(self):
        toggle_post_vote(post=self.post, user=self.user, value=-1)
        toggle_post_vote(post=self.post, user=self.user, value=-1)
        self.assertEqual(PostVote.objects.filter(post=self.post, user=self.user).count(), 0)

    def test_returns_correct_score(self):
        other = make_user("other")
        toggle_post_vote(post=self.post, user=self.user, value=1)
        score = toggle_post_vote(post=self.post, user=other, value=1)
        self.assertEqual(score, 2)

class ToggleCommentVoteTest(TestCase):

    def setUp(self):
        self.user = make_user("commvoter")
        self.community = make_community(self.user, name="cvotecomm")
        self.post = make_post(self.user, self.community)
        self.comment = make_comment(self.user, self.post)

    def test_upvote_creates_vote(self):
        toggle_comment_vote(comment=self.comment, user=self.user, value=1)
        self.assertEqual(CommentVote.objects.filter(comment=self.comment, user=self.user, value=1).count(), 1)

    def test_same_upvote_again_removes_vote(self):
        toggle_comment_vote(comment=self.comment, user=self.user, value=1)
        toggle_comment_vote(comment=self.comment, user=self.user, value=1)
        self.assertEqual(CommentVote.objects.filter(comment=self.comment, user=self.user).count(), 0)

    def test_upvote_to_downvote_changes_value(self):
        toggle_comment_vote(comment=self.comment, user=self.user, value=1)
        toggle_comment_vote(comment=self.comment, user=self.user, value=-1)
        vote = CommentVote.objects.get(comment=self.comment, user=self.user)
        self.assertEqual(vote.value, -1)

    def test_downvote_toggle_removes_vote(self):
        toggle_comment_vote(comment=self.comment, user=self.user, value=-1)
        toggle_comment_vote(comment=self.comment, user=self.user, value=-1)
        self.assertEqual(CommentVote.objects.filter(comment=self.comment, user=self.user).count(), 0)

class VotePostViewTest(TestCase):

    def setUp(self):
        self.user = make_user("viewvoter")
        self.community = make_community(self.user, name="viewvotecomm")
        self.post = make_post(self.user, self.community)
        self.client = Client()
        self.url = reverse("votes:post", kwargs={"post_id": self.post.pk})

    def test_anonymous_redirected_to_login(self):
        response = self.client.post(self.url, {"value": "up"})
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response["Location"])

    def test_authenticated_upvote_creates_vote(self):
        self.client.login(username="viewvoter", password="pass")
        self.client.post(self.url, {"value": "up"})
        self.assertEqual(PostVote.objects.filter(post=self.post, user=self.user, value=1).count(), 1)

    def test_authenticated_downvote_creates_vote(self):
        self.client.login(username="viewvoter", password="pass")
        self.client.post(self.url, {"value": "down"})
        self.assertEqual(PostVote.objects.filter(post=self.post, user=self.user, value=-1).count(), 1)  