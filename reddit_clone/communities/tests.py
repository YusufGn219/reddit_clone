from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

from communities.models import Community, CommunityModerator
from communities.utils import normalize_community_name
from communities.forms import CommunityCreateForm

User = get_user_model()

class NormalizeCommunityNameTest(TestCase):

    def test_lowercase(self):
        self.assertEqual(normalize_community_name("Django"), "django")

    def test_spaces_replaced_with_hyphen(self):
        self.assertEqual(normalize_community_name("my community"), "my-community")

    def test_multiple_spaces_single_hyphen(self):
        self.assertEqual(normalize_community_name("my  community"), "my-community")

    def test_turkish_chars_normalized(self):
        self.assertEqual(normalize_community_name("çşğüöı"), "csguo" + "i")

    def test_special_chars_stripped(self):
        self.assertEqual(normalize_community_name("hello!@#world"), "helloworld")

    def test_hyphens_allowed(self):
        result = normalize_community_name("my-community")
        self.assertIn("-", result)

    def test_underscores_allowed(self):
        result = normalize_community_name("my_community")
        self.assertIn("_", result)

    def test_none_returns_empty_string(self):
        self.assertEqual(normalize_community_name(None), "")

    def test_leading_trailing_hyphens_stripped(self):
        result = normalize_community_name("-hello-")
        self.assertFalse(result.startswith("-"))
        self.assertFalse(result.endswith("-"))

    def test_double_hyphens_collapsed(self):
        result = normalize_community_name("a--b")
        self.assertNotIn("--", result)

class CommunityCreateFormTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user("formuser", password="pass")

    def _post_form(self, name):
        return CommunityCreateForm(data={"name": name, "title": "Test Title", "description": "desc"})

    def test_valid_name_accepted(self):
        form = self._post_form("validname")
        self.assertTrue(form.is_valid())

    def test_short_name_rejected(self):
        form = self._post_form("ab")
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)

    def test_empty_name_rejected(self):
        form = self._post_form("")
        self.assertFalse(form.is_valid())

    def test_duplicate_name_rejected(self):
        Community.objects.create(name="dupname", title="T", description="d", created_by=self.user)
        form = self._post_form("dupname")
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)

    def test_turkish_name_normalized(self):
        form = self._post_form("çevre")
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "cevre")

class CommunityCreateViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user("creator", password="pass")
        self.client = Client()
        self.url = reverse("communities:create")

    def test_anonymous_redirected_to_login(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response["Location"])

    def test_authenticated_get_returns_200(self):
        self.client.login(username="creator", password="pass")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_valid_post_creates_community(self):
        self.client.login(username="creator", password="pass")
        self.client.post(self.url, {"name": "newcommunity", "title": "New Comm", "description": "desc"})
        self.assertTrue(Community.objects.filter(name="newcommunity").exists())

    def test_creator_becomes_moderator(self):
        self.client.login(username="creator", password="pass")
        self.client.post(self.url, {"name": "modcomm", "title": "Mod Comm", "description": "desc"})
        comm = Community.objects.get(name="modcomm")
        self.assertTrue(CommunityModerator.objects.filter(community=comm, user=self.user).exists())

    def test_redirect_after_create(self):
        self.client.login(username="creator", password="pass")
        response = self.client.post(self.url, {"name": "redirectcomm", "title": "R", "description": "d"})
        self.assertEqual(response.status_code, 302)

class CommunityEditPermissionTest(TestCase):

    def setUp(self):
        self.owner = User.objects.create_user("owner", password="pass")
        self.mod = User.objects.create_user("mod", password="pass")
        self.other = User.objects.create_user("other", password="pass")
        self.community = Community.objects.create(
            name="permcomm", title="Perm", description="desc", created_by=self.owner
        )
        CommunityModerator.objects.create(community=self.community, user=self.mod)
        self.edit_url = reverse("communities:edit", kwargs={"name": "permcomm"})

    def test_owner_can_edit(self):
        self.client.login(username="owner", password="pass")
        response = self.client.post(self.edit_url, {"title": "Updated", "description": "updated"})
        self.assertNotEqual(response.status_code, 403)

    def test_mod_can_edit(self):
        self.client.login(username="mod", password="pass")
        response = self.client.post(self.edit_url, {"title": "Mod Updated", "description": "x"})
        self.assertNotEqual(response.status_code, 403)

    def test_non_mod_gets_403(self):
        self.client.login(username="other", password="pass")
        response = self.client.post(self.edit_url, {"title": "Hacked", "description": "x"})
        self.assertEqual(response.status_code, 403)

    def test_anonymous_redirected(self):
        response = self.client.post(self.edit_url, {"title": "x", "description": "x"})
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response["Location"])
