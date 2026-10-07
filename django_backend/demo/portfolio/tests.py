import json
from io import StringIO
from tempfile import TemporaryDirectory

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management import call_command
from django.test import Client, TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from .models import ContactSubmission, Project, SiteProfile, Skill


class PortfolioApiTests(TestCase):
    def setUp(self):
        Project.objects.create(title="Test Project", slug="test-project", description="A test project description.", category="test-category", tech_stack=["Python"], featured=True)
        Skill.objects.create(name="Testing", category="Engineering", proficiency_level=90)

    def test_home_health_and_public_api(self):
        client = Client()
        home = client.get("/")
        self.assertEqual(home.status_code, 200)
        self.assertContains(home, "Test Project")
        self.assertContains(home, "Testing")
        self.assertEqual(client.get("/health").json()["data"]["status"], "ok")
        self.assertEqual(len(client.get("/api/projects?limit=2&category=test-category").json()["data"]), 1)
        self.assertIn("Testing", {skill["name"] for skill in client.get("/api/skills").json()["data"]})

    def test_contact_requires_csrf_and_persists(self):
        client = Client(enforce_csrf_checks=True)
        client.get("/")
        payload = {"name": "Test User", "email": "test@example.com", "subject": "Smoke test", "message": "This is a valid smoke test message."}
        self.assertEqual(client.post("/api/messages", data=json.dumps(payload), content_type="application/json").status_code, 403)
        token = client.cookies["csrftoken"].value
        response = client.post("/api/messages", data=json.dumps(payload), content_type="application/json", HTTP_X_CSRFTOKEN=token)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(ContactSubmission.objects.count(), 1)

    def test_contact_rejects_invalid_payload(self):
        client = Client()
        response = client.post("/api/messages", data=json.dumps({"name": "A", "email": "bad", "message": "short"}), content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(ContactSubmission.objects.count(), 0)


class PortfolioAdminTests(TestCase):
    def test_seed_command_preserves_admin_edited_projects(self):
        project = Project.objects.get(slug="password-strength-checker")
        project.description = "Preserve this admin edit."
        project.save(update_fields=("description",))

        call_command("seed_portfolio", stdout=StringIO())

        project.refresh_from_db()
        self.assertEqual(project.description, "Preserve this admin edit.")

    def test_contact_inbox_can_show_five_thousand_messages(self):
        admin_user = get_user_model().objects.create_superuser(
            username="inbox-admin",
            email="inbox-admin@example.com",
            password="test-only-password",
        )
        submitted_at = timezone.now()
        ContactSubmission.objects.bulk_create([
            ContactSubmission(
                name=f"Message {index}",
                email=f"message-{index}@example.com",
                message_body="A saved portfolio enquiry.",
                submitted_at=submitted_at,
            )
            for index in range(5000)
        ])
        client = Client()
        client.force_login(admin_user)

        response = client.get(reverse("admin:portfolio_contactsubmission_changelist"), {"all": "1"})

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["cl"].show_all)
        self.assertEqual(response.context["cl"].result_count, 5000)
        self.assertEqual(len(response.context["cl"].result_list), 5000)

    def test_uploaded_cv_is_available_outside_debug_mode(self):
        pdf_content = b"%PDF-1.4\nCV content\n%%EOF"
        with TemporaryDirectory() as media_root, override_settings(MEDIA_ROOT=media_root, DEBUG=False):
            profile = SiteProfile.objects.first() or SiteProfile.objects.create()
            profile.cv_file.save(
                "rainhard-cv.pdf",
                SimpleUploadedFile("rainhard-cv.pdf", pdf_content, content_type="application/pdf"),
                save=True,
            )

            response = Client().get(reverse("cv"))

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response["Content-Type"], "application/pdf")
            self.assertEqual(b"".join(response.streaming_content), pdf_content)
            self.assertEqual(Client().get(reverse("profile")).json()["data"]["cvUrl"], reverse("cv"))
