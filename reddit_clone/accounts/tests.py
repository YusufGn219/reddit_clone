from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

from communities.models import Community
from posts.models import Post

User = get_user_model()

class RegisterViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("register")

    def test_valid_registration_creates_user(self):
        self.client.post(self.url, {
            "username": "newuser",
            "password1": "StrongPass123!",
            "password2": "StrongPass123!",
        })
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_user_logged_in_after_register(self):
        response = self.client.post(self.url, {
            "username": "autologin",
            "password1": "StrongPass123!",
            "password2": "StrongPass123!",
        }, follow=True)
        self.assertTrue(response.context["user"].is_authenticated)

    def test_duplicate_username_not_created_twice(self):
        User.objects.create_user("existing", password="pass")
        self.client.post(self.url, {
            "username": "existing",
            "password1": "StrongPass123!",
            "password2": "StrongPass123!",
        })
        self.assertEqual(User.objects.filter(username="existing").count(), 1)

    def test_mismatched_passwords_rejected(self):
        self.client.post(self.url, {
            "username": "mismatch",
            "password1": "StrongPass123!",
            "password2": "WrongPass456!",
        })
        self.assertFalse(User.objects.filter(username="mismatch").exists())

    def test_register_page_loads(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def setUp(self):
        self.client = Client()
        self.url = reverse("register")
    
    def test_valid_registration_creates_user(self):
        self.client.post(self.url, {
            "username": "newuser",
            "password1": "StrongPass123!",
            "password2": "StrongPass123!",
        })
        self.assertTrue(User.objects.filter(username="newuser").exists())
        
        
    def test_duplicate_username_not_created_twice(self):
        User.objects.create_user("existing", password="pass")
        self.client.post(self.url, {
            "username": "existing",
            "password1": "StrongPass123!",
            "password2": "StrongPass123!",
        })
        self.assertEqual(User.objects.filter(username="existing").count(), 1)

    def test_mismatched_passwords_rejected(self):
        self.client.post(self.url, {
            "username": "mismatch",
            "password1": "StrongPass123!",
            "password2": "WrongPass456!",
        })
        self.assertFalse(User.objects.filter(username="mismatch").exists())

    def test_register_page_loads(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

class LoginRequiredTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user("owner", password="pass")
        self.community = Community.objects.create(
            name="logincomm", title="T", description="d", created_by=self.user
        )
        self.post = Post.objects.create(
            title="Login Post", body="b", author=self.user, community=self.community
        )

    def _assert_login_redirect(self, url, method="get", data=None):
        response = getattr(self.client, method)(url, data or {})
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response["Location"])

    def test_community_create_requires_login(self):
        self._assert_login_redirect(reverse("communities:create"))

    def test_post_create_requires_login(self):
        self._assert_login_redirect(reverse("posts:post_create"))

    def test_post_delete_requires_login(self):
        self._assert_login_redirect(
            reverse("posts:post_delete", kwargs={"post_id": self.post.pk}),
            method="post",
        )

    def test_vote_post_requires_login(self):
        self._assert_login_redirect(
            reverse("votes:post", kwargs={"post_id": self.post.pk}),
            method="post",
            data={"value": 1},
        )

class ProfileViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user("profileuser", password="pass")
        self.url = reverse("profile", kwargs={"username": "profileuser"})

    def test_profile_loads_for_anonymous(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_profile_contains_username(self):
        response = self.client.get(self.url)
        self.assertContains(response, "profileuser")

    def test_nonexistent_profile_returns_404(self):
        url = reverse("profile", kwargs={"username": "doesnotexist"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)