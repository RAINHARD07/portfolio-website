from django.db import models
from django.core.validators import FileExtensionValidator
from django.utils.text import slugify


class SiteProfile(models.Model):
    name = models.CharField(max_length=160, default="Rainhard Boah Asante")
    email = models.EmailField(default="asanteboahrainhard8@gmail.com")
    phone = models.CharField(max_length=40, default="020 537 8613")
    location = models.CharField(max_length=120, default="Kumasi, Ghana")
    cv_file = models.FileField(
        "CV upload (PDF)",
        upload_to="cv/",
        blank=True,
        validators=[FileExtensionValidator(["pdf"])],
        help_text="Upload your current CV as a PDF. This replaces the previous CV link on the website.",
    )
    instagram_url = models.URLField(default="https://www.instagram.com/aburokyire_07")
    github_url = models.URLField(default="https://github.com/RAINHARD07")
    linkedin_url = models.URLField(default="https://www.linkedin.com/in/asante-boah-rainhard-285303392/")
    x_url = models.URLField(default="https://x.com/boah_asante")
    facebook_url = models.URLField(default="https://www.facebook.com/rainhard.asante.boah")
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Project(models.Model):
    title = models.CharField(max_length=240)
    slug = models.SlugField(max_length=260, unique=True, db_index=True)
    description = models.TextField()
    category = models.CharField(max_length=80, db_index=True)
    tech_stack = models.JSONField(default=list)
    image_url = models.URLField(max_length=500, blank=True)
    project_url = models.URLField(max_length=500, blank=True)
    github_url = models.URLField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    featured = models.BooleanField(default=False, db_index=True)

    class Meta:
        ordering = ("-featured", "-created_at", "-id")
        indexes = [models.Index(fields=("featured", "-created_at", "-id")), models.Index(fields=("category", "-created_at", "-id"))]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Skill(models.Model):
    name = models.CharField(max_length=120)
    category = models.CharField(max_length=80, db_index=True)
    proficiency_level = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ("category", "-proficiency_level", "name")
        constraints = [models.UniqueConstraint(fields=("name", "category"), name="unique_skill_category")]
        indexes = [models.Index(fields=("category", "-proficiency_level"))]

    def __str__(self):
        return f"{self.name} ({self.category})"


class BlogPost(models.Model):
    title = models.CharField(max_length=240)
    slug = models.SlugField(max_length=260, unique=True, db_index=True)
    content = models.TextField()
    excerpt = models.CharField(max_length=500, blank=True)
    tags = models.JSONField(default=list)
    published_at = models.DateTimeField(null=True, blank=True, db_index=True)
    views_count = models.PositiveBigIntegerField(default=0)

    class Meta:
        ordering = ("-published_at", "-id")
        indexes = [models.Index(fields=("-published_at", "-id"))]

    def __str__(self):
        return self.title


class ContactSubmission(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField(max_length=320, db_index=True)
    subject = models.CharField(max_length=200, blank=True)
    message_body = models.TextField()
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=500, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True, db_index=True)
    is_reviewed = models.BooleanField(default=False, db_index=True)

    class Meta:
        ordering = ("-submitted_at", "-id")
        indexes = [
            models.Index(fields=("is_reviewed", "-submitted_at", "-id")),
            models.Index(fields=("-submitted_at", "-id")),
        ]

    def __str__(self):
        return f"{self.name} <{self.email}>"


class HighVolumeLogEntry(models.Model):
    action_category = models.CharField(max_length=80, db_index=True)
    description = models.CharField(max_length=500)
    visitor_ip = models.GenericIPAddressField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    metadata = models.JSONField(default=dict)

    class Meta:
        ordering = ("-timestamp", "-id")
        indexes = [models.Index(fields=("action_category", "-timestamp", "-id")), models.Index(fields=("visitor_ip", "-timestamp"))]

    def __str__(self):
        return f"{self.action_category} at {self.timestamp:%Y-%m-%d %H:%M}"
