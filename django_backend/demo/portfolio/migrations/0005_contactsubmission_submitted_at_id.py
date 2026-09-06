from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("portfolio", "0004_alter_siteprofile_cv_file")]

    operations = [
        migrations.AddIndex(
            model_name="contactsubmission",
            index=models.Index(fields=("-submitted_at", "-id"), name="portfolio_c_submitt_6539a4_idx"),
        ),
    ]