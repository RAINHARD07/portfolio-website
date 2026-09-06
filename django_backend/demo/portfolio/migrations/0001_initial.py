from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(name="BlogPost", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("title", models.CharField(max_length=240)),
            ("slug", models.SlugField(db_index=True, max_length=260, unique=True)),
            ("content", models.TextField()),
            ("excerpt", models.CharField(blank=True, max_length=500)),
            ("tags", models.JSONField(default=list)),
            ("published_at", models.DateTimeField(blank=True, db_index=True, null=True)),
            ("views_count", models.PositiveBigIntegerField(default=0)),
        ], options={"ordering": ("-published_at", "-id"), "indexes": [models.Index(fields=["-published_at", "-id"], name="portfolio_b_publishe_3c5b53_idx")]}),
        migrations.CreateModel(name="ContactSubmission", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("name", models.CharField(max_length=120)),
            ("email", models.EmailField(db_index=True, max_length=320)),
            ("subject", models.CharField(blank=True, max_length=200)),
            ("message_body", models.TextField()),
            ("ip_address", models.GenericIPAddressField(blank=True, null=True)),
            ("user_agent", models.CharField(blank=True, max_length=500)),
            ("submitted_at", models.DateTimeField(auto_now_add=True, db_index=True)),
            ("is_reviewed", models.BooleanField(db_index=True, default=False)),
        ], options={"ordering": ("-submitted_at", "-id"), "indexes": [models.Index(fields=["is_reviewed", "-submitted_at", "-id"], name="portfolio_c_is_revie_7e92b3_idx")]}),
        migrations.CreateModel(name="HighVolumeLogEntry", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("action_category", models.CharField(db_index=True, max_length=80)),
            ("description", models.CharField(max_length=500)),
            ("visitor_ip", models.GenericIPAddressField(blank=True, null=True)),
            ("timestamp", models.DateTimeField(auto_now_add=True, db_index=True)),
            ("metadata", models.JSONField(default=dict)),
        ], options={"ordering": ("-timestamp", "-id"), "indexes": [models.Index(fields=["action_category", "-timestamp", "-id"], name="portfolio_h_action_c_1d760e_idx"), models.Index(fields=["visitor_ip", "-timestamp"], name="portfolio_h_visitor__bf5c1e_idx")]}),
        migrations.CreateModel(name="Project", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("title", models.CharField(max_length=240)),
            ("slug", models.SlugField(db_index=True, max_length=260, unique=True)),
            ("description", models.TextField()),
            ("category", models.CharField(db_index=True, max_length=80)),
            ("tech_stack", models.JSONField(default=list)),
            ("image_url", models.URLField(blank=True, max_length=500)),
            ("project_url", models.URLField(blank=True, max_length=500)),
            ("github_url", models.URLField(blank=True, max_length=500)),
            ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
            ("featured", models.BooleanField(db_index=True, default=False)),
        ], options={"ordering": ("-featured", "-created_at", "-id"), "indexes": [models.Index(fields=["featured", "-created_at", "-id"], name="portfolio_p_feature_87d776_idx"), models.Index(fields=["category", "-created_at", "-id"], name="portfolio_p_category_8e8e0b_idx")]}),
        migrations.CreateModel(name="Skill", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("name", models.CharField(max_length=120)),
            ("category", models.CharField(db_index=True, max_length=80)),
            ("proficiency_level", models.PositiveSmallIntegerField(default=0)),
        ], options={"ordering": ("category", "-proficiency_level", "name"), "indexes": [models.Index(fields=["category", "-proficiency_level"], name="portfolio_s_category_79c302_idx")], "constraints": [models.UniqueConstraint(fields=("name", "category"), name="unique_skill_category")]}),
    ]
