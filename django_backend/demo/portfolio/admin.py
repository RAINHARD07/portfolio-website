from django.contrib import admin

from .models import BlogPost, ContactSubmission, HighVolumeLogEntry, Project, SiteProfile, Skill


@admin.register(SiteProfile)
class SiteProfileAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "cv_link", "updated_at")
    fieldsets = (
        ("Profile", {"fields": ("name", "email", "phone", "location", "cv_file")}),
        ("Social links", {"fields": ("instagram_url", "github_url", "linkedin_url", "x_url", "facebook_url")}),
    )

    def has_add_permission(self, request):
        return not SiteProfile.objects.exists()

    @admin.display(description="CV")
    def cv_link(self, obj):
        return "Uploaded" if obj.cv_file else "Using default CV"


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "featured", "created_at")
    list_filter = ("category", "featured", "created_at")
    search_fields = ("title", "slug", "description", "category")
    date_hierarchy = "created_at"
    list_per_page = 50
    prepopulated_fields = {"slug": ("title",)}


@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "message_preview", "is_reviewed", "submitted_at")
    list_filter = ("is_reviewed", "submitted_at")
    search_fields = ("name", "email", "subject", "message_body", "ip_address")
    date_hierarchy = "submitted_at"
    list_per_page = 50

    @admin.display(description="Message")
    def message_preview(self, obj):
        return obj.message_body[:80] + ("..." if len(obj.message_body) > 80 else "")


@admin.register(HighVolumeLogEntry)
class HighVolumeLogEntryAdmin(admin.ModelAdmin):
    list_display = ("action_category", "visitor_ip", "timestamp")
    list_filter = ("action_category", "timestamp")
    search_fields = ("action_category", "description", "visitor_ip")
    date_hierarchy = "timestamp"
    list_per_page = 100


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("title", "published_at", "views_count")
    list_filter = ("published_at",)
    search_fields = ("title", "slug", "content", "excerpt")
    date_hierarchy = "published_at"
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "proficiency_level")
    list_filter = ("category",)
    search_fields = ("name", "category")
