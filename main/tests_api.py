import uuid
import datetime

from django.contrib.auth.models import Group, User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from main.models import Project, Experience, Skill


class ProjectAPITest(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_superuser(
            username="owner", password="test-password", email="owner@example.com",
        )
        self.visitor = User.objects.create_user(username="visitor", password="test-password")
        self.project = Project.objects.create(
            title="Portfolio", description="My website", tech_stack="Django",
        )
        self.list_url = reverse("api:project-list")
        self.detail_url = reverse("api:project-detail", args=[self.project.id])
        self.star_url = reverse("api:project-star", args=[self.project.id])
        self.payload = {
            "title": "New project", "description": "A useful app", "tech_stack": "Python",
            "project_url": "https://example.com/", "project_image_url": "",
        }

    def test_public_list_and_detail(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["id"], str(self.project.id))
        self.assertFalse(response.data[0]["is_starred"])
        self.assertNotIn("fields", response.data[0])
        self.assertEqual(self.client.get(self.detail_url).status_code, status.HTTP_200_OK)

    def test_search_and_empty_results(self):
        response = self.client.get(self.list_url, {"title": "PORT"})
        self.assertEqual(len(response.data), 1)
        response = self.client.get(self.list_url, {"title": "not-found"})
        self.assertEqual(response.data, [])

    def test_missing_project(self):
        url = reverse("api:project-detail", args=[uuid.uuid4()])
        self.assertEqual(self.client.get(url).status_code, status.HTTP_404_NOT_FOUND)

    def test_guest_and_visitor_cannot_write(self):
        for user in (None, self.visitor):
            self.client.force_authenticate(user=user)
            self.assertEqual(self.client.post(self.list_url, self.payload, format="json").status_code, 403)
            self.assertEqual(self.client.patch(self.detail_url, {"title": "Changed"}, format="json").status_code, 403)
            self.assertEqual(self.client.delete(self.detail_url).status_code, 403)
        self.assertEqual(Project.objects.count(), 1)
        self.project.refresh_from_db()
        self.assertEqual(self.project.title, "Portfolio")

    def test_owner_can_create(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Project.objects.filter(pk=response.data["id"]).exists())

    def test_validation(self):
        self.client.force_authenticate(user=self.owner)
        for changes, field in [
            ({"title": "   "}, "title"),
            ({"title": '<img src="x" onerror="alert(1)">'}, "title"),
            ({"project_url": "javascript:alert(1)"}, "project_url"),
        ]:
            response = self.client.post(self.list_url, {**self.payload, **changes}, format="json")
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertIn(field, response.data)
        self.assertEqual(Project.objects.count(), 1)

    def test_patch_put_and_delete(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.patch(self.detail_url, {"title": "Changed"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.project.refresh_from_db()
        self.assertEqual(self.project.description, "My website")
        response = self.client.put(self.detail_url, {"title": "Incomplete"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.put(self.detail_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.content, b"")
        self.assertFalse(Project.objects.filter(pk=self.project.id).exists())

    def test_star_requires_login_and_toggles(self):
        self.assertEqual(self.client.post(self.star_url).status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.visitor)
        response = self.client.post(self.star_url)
        self.assertTrue(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 1)
        response = self.client.post(self.star_url)
        self.assertFalse(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 0)

    def test_computed_fields_are_read_only(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, {
            **self.payload, "star_count": 99, "is_starred": True,
            "starred_by_names": "forged", "starred_by": [self.visitor.id],
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["star_count"], 0)
        self.assertFalse(response.data["is_starred"])

    def test_staff_and_editor_cannot_manage_tutorial_projects(self):
        self.visitor.is_staff = True
        self.visitor.save()
        self.visitor.groups.add(Group.objects.create(name="Editor"))
        self.client.force_authenticate(user=self.visitor)
        response = self.client.patch(self.detail_url, {"title": "Changed"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_wrong_method(self):
        self.client.force_authenticate(user=self.owner)
        self.assertEqual(self.client.delete(self.list_url).status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_session_write_without_csrf_is_rejected(self):
        client = APIClient(enforce_csrf_checks=True)
        self.assertTrue(client.login(username="owner", password="test-password"))
        response = client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Project.objects.count(), 1)

    def test_session_write_with_csrf_succeeds(self):
        client = APIClient(enforce_csrf_checks=True)
        client.login(username="owner", password="test-password")
        # The Browsable API form renders a real CSRF token into the response.
        page = client.get(self.list_url, HTTP_ACCEPT="text/html")
        self.assertEqual(page.status_code, status.HTTP_200_OK)
        token = client.cookies["csrftoken"].value
        response = client.post(
            self.list_url, self.payload, format="json", HTTP_X_CSRFTOKEN=token,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class ResourceAPITestMixin:
    """Role, validation, star and CSRF checks shared by Skill and Experience."""

    model = None
    url_prefix = None       # "skill" -> api:skill-list / -detail / -star
    search_param = None
    search_field = None
    payload = None          # a complete, valid create/replace body
    patch_field = None
    invalid_cases = ()      # (overrides, field expected in the 400 body)

    def make_object(self):
        raise NotImplementedError

    def setUp(self):
        super().setUp()
        self.owner = User.objects.create_superuser(
            username="owner", password="test-password", email="owner@example.com",
        )
        self.user = User.objects.create_user(
            username="regular", password="test-password", email="regular@example.com",
        )
        self.editor = User.objects.create_user(username="editor", password="test-password")
        self.editor.groups.add(Group.objects.create(name="Editor"))
        self.obj = self.make_object()
        self.list_url = reverse(f"api:{self.url_prefix}-list")
        self.detail_url = reverse(f"api:{self.url_prefix}-detail", args=[self.obj.id])
        self.star_url = reverse(f"api:{self.url_prefix}-star", args=[self.obj.id])

    def stored_value(self):
        self.obj.refresh_from_db()
        return getattr(self.obj, self.patch_field)

    # --- Reading ---

    def test_guest_can_read_list_and_detail(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["id"], str(self.obj.id))
        self.assertFalse(response.data[0]["is_starred"])
        self.assertNotIn("fields", response.data[0])
        self.assertEqual(self.client.get(self.detail_url).status_code, status.HTTP_200_OK)

    def test_search_and_empty_results(self):
        term = getattr(self.obj, self.search_field)[:3].upper()
        response = self.client.get(self.list_url, {self.search_param: term})
        self.assertEqual(len(response.data), 1)
        response = self.client.get(self.list_url, {self.search_param: "not-found"})
        self.assertEqual(response.data, [])

    def test_missing_object_returns_404(self):
        url = reverse(f"api:{self.url_prefix}-detail", args=[uuid.uuid4()])
        self.assertEqual(self.client.get(url).status_code, status.HTTP_404_NOT_FOUND)

    def test_wrong_method_returns_405(self):
        self.client.force_authenticate(user=self.owner)
        self.assertEqual(
            self.client.delete(self.list_url).status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    def test_response_never_exposes_account_data(self):
        self.client.force_authenticate(user=self.user)
        self.client.post(self.star_url)
        body = self.client.get(self.list_url).content.decode()
        for secret in ("example.com", "pbkdf2", "password"):
            self.assertNotIn(secret, body)

    # --- Roles ---

    def test_guest_and_regular_user_cannot_write(self):
        original = self.stored_value()
        for user in (None, self.user):
            self.client.force_authenticate(user=user)
            self.assertEqual(
                self.client.post(self.list_url, self.payload, format="json").status_code, 403)
            self.assertEqual(
                self.client.patch(self.detail_url, {self.patch_field: "Changed"}, format="json").status_code, 403)
            self.assertEqual(
                self.client.put(self.detail_url, self.payload, format="json").status_code, 403)
            self.assertEqual(self.client.delete(self.detail_url).status_code, 403)
        self.assertEqual(self.model.objects.count(), 1)
        self.assertEqual(self.stored_value(), original)

    def test_editor_can_patch_and_put(self):
        self.client.force_authenticate(user=self.editor)
        response = self.client.patch(self.detail_url, {self.patch_field: "Edited"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.stored_value(), "Edited")
        response = self.client.put(self.detail_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.stored_value(), self.payload[self.patch_field])

    def test_editor_cannot_create_or_delete(self):
        self.client.force_authenticate(user=self.editor)
        self.assertEqual(
            self.client.post(self.list_url, self.payload, format="json").status_code, 403)
        self.assertEqual(self.client.delete(self.detail_url).status_code, 403)
        self.assertEqual(self.model.objects.count(), 1)
        self.assertTrue(self.model.objects.filter(pk=self.obj.pk).exists())

    def test_owner_can_create_replace_and_delete(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(self.model.objects.filter(pk=response.data["id"]).exists())
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.content, b"")
        self.assertFalse(self.model.objects.filter(pk=self.obj.pk).exists())

    def test_put_requires_every_field(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.put(self.detail_url, {self.patch_field: "Only one"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # --- Validation ---

    def test_invalid_input_returns_400_and_changes_nothing(self):
        self.client.force_authenticate(user=self.owner)
        original = self.stored_value()
        for changes, field in self.invalid_cases:
            with self.subTest(changes=changes):
                response = self.client.post(self.list_url, {**self.payload, **changes}, format="json")
                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
                self.assertIn(field, response.data)
        self.assertEqual(self.model.objects.count(), 1)
        self.assertEqual(self.stored_value(), original)

    def test_html_is_stripped_from_text(self):
        self.client.force_authenticate(user=self.owner)
        marked_up = f"<b>{self.payload[self.patch_field]}</b><script>alert(1)</script>"
        response = self.client.post(
            self.list_url, {**self.payload, self.patch_field: marked_up}, format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        saved = self.model.objects.get(pk=response.data["id"])
        self.assertNotIn("<", getattr(saved, self.patch_field))

    def test_computed_fields_are_read_only(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, {
            **self.payload, "star_count": 99, "is_starred": True,
            "starred_by_names": "forged", "starred_by": [self.user.id],
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["star_count"], 0)
        self.assertFalse(response.data["is_starred"])
        self.assertEqual(response.data["starred_by_names"], "")

    # --- Star ---

    def test_guest_cannot_star(self):
        self.assertEqual(self.client.post(self.star_url).status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.obj.starred_by.count(), 0)

    def test_star_toggles_for_the_logged_in_account(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.star_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 1)
        self.assertEqual(list(self.obj.starred_by.all()), [self.user])
        response = self.client.post(self.star_url)
        self.assertFalse(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 0)
        self.assertEqual(self.obj.starred_by.count(), 0)

    def test_editor_can_star(self):
        self.client.force_authenticate(user=self.editor)
        self.assertEqual(self.client.post(self.star_url).status_code, status.HTTP_200_OK)

    def test_star_state_is_per_account(self):
        self.client.force_authenticate(user=self.user)
        self.client.post(self.star_url)
        self.client.force_authenticate(user=self.editor)
        response = self.client.get(self.detail_url)
        self.assertEqual(response.data["star_count"], 1)
        self.assertFalse(response.data["is_starred"])

    # --- CSRF ---

    def test_session_write_without_csrf_token_is_rejected(self):
        client = APIClient(enforce_csrf_checks=True)
        self.assertTrue(client.login(username="owner", password="test-password"))
        original = self.stored_value()
        self.assertEqual(client.post(self.list_url, self.payload, format="json").status_code, 403)
        self.assertEqual(
            client.patch(self.detail_url, {self.patch_field: "Changed"}, format="json").status_code, 403)
        self.assertEqual(client.delete(self.detail_url).status_code, 403)
        self.assertEqual(client.post(self.star_url).status_code, 403)
        self.assertEqual(self.model.objects.count(), 1)
        self.assertEqual(self.stored_value(), original)
        self.assertEqual(self.obj.starred_by.count(), 0)

    def test_session_write_with_csrf_token_succeeds(self):
        client = APIClient(enforce_csrf_checks=True)
        client.login(username="owner", password="test-password")
        # The Browsable API renders a real CSRF token and sets the cookie.
        self.assertEqual(client.get(self.list_url, HTTP_ACCEPT="text/html").status_code, 200)
        token = client.cookies["csrftoken"].value
        response = client.post(self.list_url, self.payload, format="json", HTTP_X_CSRFTOKEN=token)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class SkillAPITest(ResourceAPITestMixin, APITestCase):
    model = Skill
    url_prefix = "skill"
    search_param = "name"
    search_field = "name"
    patch_field = "name"
    payload = {
        "name": "Rust", "description": "Systems programming", "category": "languages",
        "nilai": 70, "skill_image_url": "https://example.com/rust.svg",
    }
    invalid_cases = [
        ({"name": "   "}, "name"),
        ({"name": "<b></b>"}, "name"),
        ({"description": "<i></i>"}, "description"),
        ({"nilai": 0}, "nilai"),
        ({"nilai": 101}, "nilai"),
        ({"category": "nope"}, "category"),
        ({"skill_image_url": "javascript:alert(1)"}, "skill_image_url"),
    ]

    def make_object(self):
        return Skill.objects.create(
            name="Python", description="Scripting", category="languages", nilai=80,
        )

    def test_response_includes_category_label_and_groups_order(self):
        Skill.objects.create(name="Git", description="VCS", category="tools")
        response = self.client.get(self.list_url)
        self.assertEqual(response.data[0]["category_display"], "Programming Language")
        self.assertEqual([s["category"] for s in response.data], ["languages", "tools"])


class ExperienceAPITest(ResourceAPITestMixin, APITestCase):
    model = Experience
    url_prefix = "experience"
    search_param = "title"
    search_field = "title"
    patch_field = "title"
    payload = {
        "title": "Staff Acara", "description": "Mengurus acara", "category": "committee",
        "thumbnail": "", "started_at": "2025-01-01", "ended_at": None,
    }
    invalid_cases = [
        ({"title": "   "}, "title"),
        ({"title": '<img src="x" onerror="alert(1)">'}, "title"),
        ({"description": "<i></i>"}, "description"),
        ({"category": "nope"}, "category"),
        ({"thumbnail": "javascript:alert(1)"}, "thumbnail"),
        ({"ended_at": "2024-12-31"}, "ended_at"),
    ]

    def make_object(self):
        return Experience.objects.create(
            title="Asisten Dosen", description="Membantu mahasiswa", category="part-time",
            started_at=datetime.date(2025, 6, 1),
        )

    def test_started_at_is_required(self):
        self.client.force_authenticate(user=self.owner)
        body = {k: v for k, v in self.payload.items() if k != "started_at"}
        response = self.client.post(self.list_url, body, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("started_at", response.data)

    def test_is_ongoing_is_computed_and_read_only(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.patch(
            self.detail_url, {"is_ongoing": False, "ended_at": "2025-12-31"}, format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data["is_ongoing"])
        response = self.client.patch(self.detail_url, {"ended_at": None}, format="json")
        self.assertTrue(response.data["is_ongoing"])

    def test_patch_cannot_move_end_before_stored_start(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.patch(self.detail_url, {"ended_at": "2025-01-01"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("ended_at", response.data)
        self.obj.refresh_from_db()
        self.assertIsNone(self.obj.ended_at)

    def test_patch_other_field_does_not_revalidate_dates(self):
        Experience.objects.filter(pk=self.obj.pk).update(ended_at=datetime.date(2020, 1, 1))
        self.client.force_authenticate(user=self.owner)
        response = self.client.patch(self.detail_url, {"title": "Renamed"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)