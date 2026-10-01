from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils.text import slugify
from django.utils import timezone

from portfolio.models import BlogPost, Project, Skill


class Command(BaseCommand):
    help = "Load the portfolio's initial projects, skills, and blog posts."

    def handle(self, *args, **options):
        skills = [
            ("Networking", "Networking", 85),
            ("IT Support", "IT Support", 90),
            ("Systems Admin", "Systems Administration", 78),
            ("Cybersecurity", "Cybersecurity", 74),
            ("Cloud Fundamentals", "Cloud", 68),
        ]
        for name, category, proficiency_level in skills:
            Skill.objects.get_or_create(name=name, category=category, defaults={"proficiency_level": proficiency_level})
        projects = [
            ("Mining Fraudulent Accounts in Large-Scale Mobile Social Networks Using Machine Learning", "machine-learning", "Compared Random Forest, Decision Tree and Logistic Regression models to surface suspicious account patterns for review.", ["Python", "Machine Learning", "Research"], True),
            ("Password Strength Checker", "security", "A local-first password feedback utility.", ["JavaScript", "Security"], False),
            ("Phishing Email Analyzer", "security", "A practical first-pass phishing triage tool.", ["JavaScript", "Security"], False),
            ("AWS EC2 Personal Cloud Security Lab", "cloud", "A repeatable EC2 hardening practice environment.", ["AWS", "EC2", "Cloud Security"], False),
        ]
        for title, category, description, tech_stack, featured in projects:
            Project.objects.get_or_create(slug=slugify(title), defaults={"title": title, "category": category, "description": description, "tech_stack": tech_stack, "featured": featured})
        for index in range(1, 21):
            BlogPost.objects.get_or_create(slug=f"systems-note-{index}", defaults={"title": f"Systems note {index}", "content": "A short operational note about dependable IT systems.", "excerpt": "A practical note about dependable systems.", "tags": ["systems", "it-support"], "published_at": timezone.now() - timedelta(days=index - 1)})
        self.stdout.write(self.style.SUCCESS("Portfolio data seeded."))
