from django.db import migrations, models
from django.core.validators import FileExtensionValidator


class Migration(migrations.Migration):
    dependencies = [("portfolio", "0003_siteprofile")]

    operations = [
        migrations.AlterField(
            model_name="siteprofile",
            name="cv_file",
            field=models.FileField(
                blank=True,
                help_text="Upload your current CV as a PDF. This replaces the previous CV link on the website.",
                upload_to="cv/",
                validators=[FileExtensionValidator(["pdf"])],
                verbose_name="CV upload (PDF)",
            ),
        ),
    ]