from django.conf import settings
from django.urls import path, re_path
from django.views.static import serve

from .views import BlogListView, ContactSubmissionView, HealthView, HomeView, ProfileView, ProjectListView, SkillListView, VisitLogView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("favicon.ico", serve, {"document_root": settings.SITE_ROOT / "Images", "path": "Asante.jpeg"}),
    re_path(r"^static/portfolio/images/(?P<path>.*)$", serve, {"document_root": settings.BASE_DIR.parent.parent / "Images"}),
    path("health", HealthView.as_view(), name="health"),
    path("api/profile", ProfileView.as_view(), name="profile"),
    path("api/projects", ProjectListView.as_view(), name="projects"),
    path("api/blog", BlogListView.as_view(), name="blog"),
    path("api/skills", SkillListView.as_view(), name="skills"),
    path("api/messages", ContactSubmissionView.as_view(), name="messages"),
    path("api/analytics/visit", VisitLogView.as_view(), name="visit"),
]
