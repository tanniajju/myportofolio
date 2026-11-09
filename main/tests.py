from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta

from main.models import Experience, Skill


class MainTest(TestCase):
    def setUp(self):
        self.experience = Experience.objects.create(
            title="Asisten Dosen PBP",
            description="Membantu mahasiswa memahami pengembangan web.",
            category="part-time",
            ended_at=None,
    )

    def test_main_url_is_accessible(self):
        response = self.client.get(reverse("main:show_main"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertNotContains(response, self.experience.title)
        self.assertContains(response, f'href="{reverse("main:show_experience")}"')

    def test_nonexistent_page_returns_404(self):
        response = self.client.get("/halaman-yang-tidak-ada/")

        self.assertEqual(response.status_code, 404)

    def test_experience_model(self):
        self.assertEqual(str(self.experience), "Asisten Dosen PBP")
        self.assertEqual(self.experience.category, "part-time")
        self.assertTrue(self.experience.is_ongoing)

    def test_experience_page(self):
        response = self.client.get(reverse("main:show_experience"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience.html")
        self.assertContains(response, f'href="{reverse("main:show_main")}"')

    def test_experience_json(self):
        response = self.client.get(reverse("main:get_experiences_json"))
        self.assertEqual(response.status_code, 200)
        fields = response.json()[0]["fields"]
        self.assertEqual(fields["title"], self.experience.title)
        self.assertEqual(fields["description"], self.experience.description)
        self.assertTrue(fields["is_ongoing"])

    def test_empty_experience_json(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:get_experiences_json"))
        self.assertEqual(response.json(), [])

    def test_empty_experience_page(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:show_experience"))

        self.assertContains(response, "Belum ada experience yang ditambahkan atau ditemukan.")

    def test_completed_experience(self):
        self.experience.ended_at = timezone.now().date() - timedelta(days=1)
        self.experience.save()
        response = self.client.get(reverse("main:get_experiences_json"))

        self.assertFalse(self.experience.is_ongoing)
        self.assertFalse(response.json()[0]["fields"]["is_ongoing"])


class SkillTest(TestCase):
    def setUp(self):
        self.skill = Skill.objects.create(
            name="CSS",
            category="languages",
            skill_image_url="www.apaaja.oke",
        )
        
    def test_skills_url_is_accessible(self):
        response = self.client.get(reverse("main:show_skill"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "skill.html")
        self.assertContains(response, f'href="{reverse("main:show_main")}"')
        # The list is loaded through the API, so the page only points to it.
        self.assertContains(response, reverse("api:skill-list"))
        api_response = self.client.get(reverse("api:skill-list"))
        self.assertEqual(api_response.json()[0]["name"], self.skill.name)

    def test_nonexistent_page_returns_404(self):
        response = self.client.get("/halaman-yang-tidak-ada/")

        self.assertEqual(response.status_code, 404)

    def test_skill_model(self):
        self.assertEqual(str(self.skill), "CSS")
        self.assertEqual(self.skill.category, "languages")
        self.assertEqual(self.skill.skill_image_url, "www.apaaja.oke")

    def test_skill_page(self):
        response = self.client.get(reverse("main:show_skill"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "skill.html")
        item = self.client.get(reverse("api:skill-list")).json()[0]
        self.assertEqual(item["name"], "CSS")
        self.assertEqual(item["description"], self.skill.description)
        self.assertContains(response, f'href="{reverse("main:show_main")}"')

    def test_empty_skill_page(self):
        Skill.objects.all().delete()
        response = self.client.get(reverse("main:show_skill"))

        self.assertContains(response, "Belum ada keahlian yang ditambahkan.")