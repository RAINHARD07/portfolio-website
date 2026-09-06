import json

from django.test import Client, TestCase

from .models import ContactSubmission, Project, Skill


class PortfolioApiTests(TestCase):
    def setUp(self):
        Project.objects.create(title="Test Project", slug="test-project", description="A test project description.", category="security", tech_stack=["Python"], featured=True)
        Skill.objects.create(name="Testing", category="Engineering", proficiency_level=90)

    def test_home_health_and_public_api(self):
        client = Client()
        home = client.get("/")
        self.assertEqual(home.status_code, 200)
        self.assertContains(home, "Test Project")
        self.assertContains(home, "Testing")
        self.assertEqual(client.get("/health").json()["data"]["status"], "ok")
        self.assertEqual(len(client.get("/api/projects?limit=2").json()["data"]), 1)
        self.assertEqual(client.get("/api/skills").json()["data"][0]["name"], "Testing")

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
