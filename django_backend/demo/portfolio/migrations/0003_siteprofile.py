from django.db import migrations, models


def create_default_profile(apps, schema_editor):
    apps.get_model("portfolio", "SiteProfile").objects.get_or_create(id=1)


class Migration(migrations.Migration):
    dependencies = [("portfolio", "0002_rename_portfolio_b_publishe_3c5b53_idx_portfolio_b_publish_b030df_idx_and_more")]

    operations = [
        migrations.CreateModel(
            name="SiteProfile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(default="Rainhard Boah Asante", max_length=160)),
                ("email", models.EmailField(default="asanteboahrainhard8@gmail.com", max_length=254)),
                ("phone", models.CharField(default="020 537 8613", max_length=40)),
                ("location", models.CharField(default="Kumasi, Ghana", max_length=120)),
                ("cv_file", models.FileField(blank=True, upload_to="cv/")),
                ("instagram_url", models.URLField(default="https://www.instagram.com/aburokyire_07")),
                ("github_url", models.URLField(default="https://github.com/RAINHARD07")),
                ("linkedin_url", models.URLField(default="https://www.linkedin.com/in/asante-boah-rainhard-285303392/")),
                ("x_url", models.URLField(default="https://x.com/boah_asante")),
                ("facebook_url", models.URLField(default="https://www.facebook.com/rainhard.asante.boah")),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.RunPython(create_default_profile, migrations.RunPython.noop),
    ]