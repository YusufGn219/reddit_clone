from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.conf import settings

from communities.models import Community
from posts.models import Post, Comment
from votes.models import PostVote, CommentVote
from votes.services import toggle_post_vote, toggle_comment_vote

User = get_user_model()


# ---------- factories/helpers ----------

def make_user(username, password="pass"):
    # safer for custom user models
    return User.objects.create_user(username=username, password=password)


def make_community(user, name="testcomm"):
    return Community.objects.create(
        name=name,
        title="T",
        description="d",
        created_by=user
    )


def make_post(user, community, title="Test Post"):
    return Post.objects.create(
        title=title,
        body="body",
        author=user,
        community=community
    )


def make_comment(user, post, body="A comment"):
    return Comment.objects.create(
        body=body,
        author=user,
        post=post
    )


# ---------- service tests ----------

class TogglePostVoteTest(TestCase):
    def setUp(self):
        self.user = make_user("voter")
        self.community = make_community(self.user)
        self.post = make_post(self.user, self.community)

    def test_upvote_creates_vote(self):
        toggle_post_vote(post=self.post, user=self.user, value=1)
        self.assertEqual(
            PostVote.objects.filter(post=self.post, user=self.user, value=1).count(),
            1
        )

    def test_same_upvote_again_removes_vote(self):
        toggle_post_vote(post=self.post, user=self.user, value=1)
        toggle_post_vote(post=self.post, user=self.user, value=1)
        self.assertEqual(
            PostVote.objects.filter(post=self.post, user=self.user).count(),
            0
        )

    def test_upvote_to_downvote_changes_value(self):
        toggle_post_vote(post=self.post, user=self.user, value=1)
        toggle_post_vote(post=self.post, user=self.user, value=-1)
        vote = PostVote.objects.get(post=self.post, user=self.user)
        self.assertEqual(vote.value, -1)

    def test_downvote_creates_vote(self):
        toggle_post_vote(post=self.post, user=self.user, value=-1)
        self.assertEqual(
            PostVote.objects.filter(post=self.post, user=self.user, value=-1).count(),
            1
        )

    def test_same_downvote_again_removes_vote(self):
        toggle_post_vote(post=self.post, user=self.user, value=-1)
        toggle_post_vote(post=self.post, user=self.user, value=-1)
        self.assertEqual(
            PostVote.objects.filter(post=self.post, user=self.user).count(),
            0
        )

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
        self.assertEqual(
            CommentVote.objects.filter(comment=self.comment, user=self.user, value=1).count(),
            1
        )

    def test_same_upvote_again_removes_vote(self):
        toggle_comment_vote(comment=self.comment, user=self.user, value=1)
        toggle_comment_vote(comment=self.comment, user=self.user, value=1)
        self.assertEqual(
            CommentVote.objects.filter(comment=self.comment, user=self.user).count(),
            0
        )

    def test_upvote_to_downvote_changes_value(self):
        toggle_comment_vote(comment=self.comment, user=self.user, value=1)
        toggle_comment_vote(comment=self.comment, user=self.user, value=-1)
        vote = CommentVote.objects.get(comment=self.comment, user=self.user)
        self.assertEqual(vote.value, -1)

    def test_downvote_toggle_removes_vote(self):
        toggle_comment_vote(comment=self.comment, user=self.user, value=-1)
        toggle_comment_vote(comment=self.comment, user=self.user, value=-1)
        self.assertEqual(
            CommentVote.objects.filter(comment=self.comment, user=self.user).count(),
            0
        )


# ---------- view tests ----------

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
        # robust against different login url names
        self.assertIn(settings.LOGIN_URL, response["Location"])

    def test_authenticated_upvote_creates_vote(self):
        ok = self.client.login(username="viewvoter", password="pass")
        self.assertTrue(ok)

        resp = self.client.post(self.url, {"value": "up"})
        self.assertIn(resp.status_code, (200, 302))

        self.assertEqual(
            PostVote.objects.filter(post=self.post, user=self.user, value=1).count(),
            1
        )

    def test_authenticated_downvote_creates_vote(self):
        ok = self.client.login(username="viewvoter", password="pass")
        self.assertTrue(ok)

        resp = self.client.post(self.url, {"value": "down"})
        self.assertIn(resp.status_code, (200, 302))

        self.assertEqual(
            PostVote.objects.filter(post=self.post, user=self.user, value=-1).count(),
            1
        )

    def test_authenticated_upvote_twice_removes_vote(self):
        ok = self.client.login(username="viewvoter", password="pass")
        self.assertTrue(ok)

        self.client.post(self.url, {"value": "up"})
        self.client.post(self.url, {"value": "up"})

        self.assertEqual(
            PostVote.objects.filter(post=self.post, user=self.user).count(),
            0
        )

    def test_authenticated_upvote_then_downvote_changes_value(self):
        ok = self.client.login(username="viewvoter", password="pass")
        self.assertTrue(ok)

        self.client.post(self.url, {"value": "up"})
        self.client.post(self.url, {"value": "down"})

        vote = PostVote.objects.get(post=self.post, user=self.user)
        self.assertEqual(vote.value, -1)


class VoteCommentViewTest(TestCase):
    """
    Eğer comment vote view'ün URL name'i farklıysa reverse kısmını projene göre değiştir.
    Ben en yaygın olanı varsaydım: votes:comment (kwargs={"comment_id": ...})
    """
    def setUp(self):
        self.user = make_user("viewcommvoter")
        self.community = make_community(self.user, name="viewcommvotecomm")
        self.post = make_post(self.user, self.community)
        self.comment = make_comment(self.user, self.post)
        self.client = Client()

        # Eğer sende isim farklıysa burayı değiştir:
        self.url = reverse("votes:comment", kwargs={"comment_id": self.comment.pk})

    def test_anonymous_redirected_to_login(self):
        response = self.client.post(self.url, {"value": "up"})
        self.assertEqual(response.status_code, 302)
        self.assertIn(settings.LOGIN_URL, response["Location"])

    def test_authenticated_upvote_creates_vote(self):
        ok = self.client.login(username="viewcommvoter", password="pass")
        self.assertTrue(ok)

        resp = self.client.post(self.url, {"value": "up"})
        self.assertIn(resp.status_code, (200, 302))

        self.assertEqual(
            CommentVote.objects.filter(comment=self.comment, user=self.user, value=1).count(),
            1
        )

    def test_authenticated_downvote_creates_vote(self):
        ok = self.client.login(username="viewcommvoter", password="pass")
        self.assertTrue(ok)

        resp = self.client.post(self.url, {"value": "down"})
        self.assertIn(resp.status_code, (200, 302))

        self.assertEqual(
            CommentVote.objects.filter(comment=self.comment, user=self.user, value=-1).count(),
            1
        )

    def test_authenticated_upvote_twice_removes_vote(self):
        ok = self.client.login(username="viewcommvoter", password="pass")
        self.assertTrue(ok)

        self.client.post(self.url, {"value": "up"})
        self.client.post(self.url, {"value": "up"})

        self.assertEqual(
            CommentVote.objects.filter(comment=self.comment, user=self.user).count(),
            0
        )

    def test_authenticated_upvote_then_downvote_changes_value(self):
        ok = self.client.login(username="viewcommvoter", password="pass")
        self.assertTrue(ok)

        self.client.post(self.url, {"value": "up"})
        self.client.post(self.url, {"value": "down"})

        vote = CommentVote.objects.get(comment=self.comment, user=self.user)
        self.assertEqual(vote.value, -1)