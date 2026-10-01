from django.db import migrations


def create_default_portfolio(apps, schema_editor):
    alias = schema_editor.connection.alias
    Project = apps.get_model("portfolio", "Project")
    Skill = apps.get_model("portfolio", "Skill")

    skills = [
        ("Networking", "Networking", 85),
        ("IT Support", "IT Support", 90),
        ("Systems Admin", "Systems Administration", 78),
        ("Cybersecurity", "Cybersecurity", 74),
        ("Cloud Fundamentals", "Cloud", 68),
    ]
    for name, category, proficiency_level in skills:
        Skill.objects.using(alias).get_or_create(
            name=name,
            category=category,
            defaults={"proficiency_level": proficiency_level},
        )

    projects = [
        (
            "Mining Fraudulent Accounts in Large-Scale Mobile Social Networks Using Machine Learning",
            "mining-fraudulent-accounts-in-large-scale-mobile-social-networks-using-machine-learning",
            "machine-learning",
            "Compared Random Forest, Decision Tree and Logistic Regression models to surface suspicious account patterns for review.",
            ["Python", "Machine Learning", "Research"],
            True,
        ),
        (
            "Password Strength Checker",
            "password-strength-checker",
            "security",
            "A local-first password feedback utility.",
            ["JavaScript", "Security"],
            False,
        ),
        (
            "Phishing Email Analyzer",
            "phishing-email-analyzer",
            "security",
            "A practical first-pass phishing triage tool.",
            ["JavaScript", "Security"],
            False,
        ),
        (
            "AWS EC2 Personal Cloud Security Lab",
            "aws-ec2-personal-cloud-security-lab",
            "cloud",
            "A repeatable EC2 hardening practice environment.",
            ["AWS", "EC2", "Cloud Security"],
            False,
        ),
    ]
    for title, slug, category, description, tech_stack, featured in projects:
        Project.objects.using(alias).get_or_create(
            slug=slug,
            defaults={
                "title": title,
                "category": category,
                "description": description,
                "tech_stack": tech_stack,
                "featured": featured,
            },
        )


class Migration(migrations.Migration):
    dependencies = [("portfolio", "0005_contactsubmission_submitted_at_id")]

    operations = [migrations.RunPython(create_default_portfolio, migrations.RunPython.noop)]