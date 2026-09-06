from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from demo.portfolio.models import BlogPost, Project, Skill


class Command(BaseCommand):
    help = "Load the portfolio's initial projects, skills, and blog posts."

    def handle(self, *args, **options):
        skills = [
            ("LAN/WAN", "Networking", 85), ("IP addressing", "Networking", 82),
            ("IT troubleshooting", "IT Support", 90), ("Windows/Linux", "Systems Administration", 78),
            ("Threat monitoring", "Cybersecurity", 74), ("AWS EC2", "Cloud", 68),
        ]
        for name, category, proficiency_level in skills:
            Skill.objects.update_or_create(name=name, category=category, defaults={"proficiency_level": proficiency_level})
        projects = [
            ("Password Strength Checker", "security", "A local-first password feedback utility.", ["JavaScript", "Security"], True),
            ("Phishing Email Analyzer", "security", "A practical first-pass phishing triage tool.", ["JavaScript", "Security"], False),
            ("AWS EC2 Personal Cloud Security Lab", "cloud", "A repeatable EC2 hardening practice environment.", ["AWS", "EC2", "Cloud Security"], False),
        ]
        for title, category, description, tech_stack, featured in projects:
            Project.objects.update_or_create(title=title, defaults={"slug": title.lower().replace(" ", "-"), "category": category, "description": description, "tech_stack": tech_stack, "featured": featured})
        for index in range(1, 21):
            BlogPost.objects.update_or_create(slug=f"systems-note-{index}", defaults={"title": f"Systems note {index}", "content": "A short operational note about dependable IT systems.", "excerpt": "A practical note about dependable systems.", "tags": ["systems", "it-support"], "published_at": timezone.now() - timedelta(days=index - 1)})
        self.stdout.write(self.style.SUCCESS("Portfolio data seeded."))
