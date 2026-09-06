import base64
import json
from datetime import datetime

from django.core.cache import cache
from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.views import View
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator

from .forms import ContactSubmissionForm
from .models import BlogPost, ContactSubmission, HighVolumeLogEntry, Project, SiteProfile, Skill

MAX_PAGE_SIZE = 100


def _cursor_encode(item):
    values = {
        "featured": int(item.featured),
        "created_at": item.created_at.isoformat(),
        "id": item.id,
    }
    return base64.urlsafe_b64encode(json.dumps(values).encode()).decode()


def _cursor_decode(value):
    try:
        decoded = base64.urlsafe_b64decode(value.encode()).decode()
        payload = json.loads(decoded)
        return int(payload["featured"]), datetime.fromisoformat(payload["created_at"]), int(payload["id"])
    except (ValueError, KeyError, TypeError, json.JSONDecodeError):
        return None


def _blog_cursor_encode(item):
    values = {"published_at": item.published_at.isoformat(), "id": item.id}
    return base64.urlsafe_b64encode(json.dumps(values).encode()).decode()


def _blog_cursor_decode(value):
    try:
        decoded = base64.urlsafe_b64decode(value.encode()).decode()
        payload = json.loads(decoded)
        return datetime.fromisoformat(payload["published_at"]), int(payload["id"])
    except (ValueError, KeyError, TypeError, json.JSONDecodeError):
        return None


def _page_size(request):
    try:
        return min(max(int(request.GET.get("limit", 20)), 1), MAX_PAGE_SIZE)
    except (TypeError, ValueError):
        return 20


def _error(message, status=400):
    return JsonResponse({"error": {"code": "VALIDATION_ERROR", "message": message}}, status=status)


def _client_ip(request):
    forwarded = request.META.get("HTTP_X_FORWARDED_FOR", "")
    return (forwarded.split(",")[0].strip() if forwarded else request.META.get("REMOTE_ADDR")) or None


@method_decorator(ensure_csrf_cookie, name="dispatch")
class HomeView(View):
    def get(self, request):
        projects = Project.objects.only(
            "id", "title", "slug", "description", "category", "tech_stack",
            "project_url", "featured",
        ).order_by("-featured", "-created_at", "-id")
        skills = Skill.objects.only("id", "name", "category", "proficiency_level").order_by(
            "category", "-proficiency_level", "name",
        )
        return render(request, "index.html", {"projects": projects, "skills": skills, "profile": SiteProfile.objects.first()})


class HealthView(View):
    def get(self, request):
        return JsonResponse({"data": {"status": "ok", "service": "portfolio-django"}})


class ProfileView(View):
    def get(self, request):
        profile = SiteProfile.objects.first()
        if profile is None:
            return JsonResponse({"data": {}})
        return JsonResponse({"data": {
            "cvUrl": profile.cv_file.url if profile.cv_file else "/static/site/cv.pdf",
            "instagramUrl": profile.instagram_url,
            "githubUrl": profile.github_url,
            "linkedinUrl": profile.linkedin_url,
            "xUrl": profile.x_url,
            "facebookUrl": profile.facebook_url,
        }})


class ProjectListView(View):
    def get(self, request):
        limit = _page_size(request)
        queryset = Project.objects.only("id", "title", "slug", "description", "category", "tech_stack", "image_url", "project_url", "github_url", "created_at", "featured")
        category = request.GET.get("category", "").strip()[:80]
        if category:
            queryset = queryset.filter(category=category)
        cursor = _cursor_decode(request.GET.get("cursor", "")) if request.GET.get("cursor") else None
        if request.GET.get("cursor") and cursor is None:
            return _error("Invalid pagination cursor.")
        if cursor:
            featured, created_at, item_id = cursor
            queryset = queryset.filter(Q(featured__lt=featured) | Q(featured=featured, created_at__lt=created_at) | Q(featured=featured, created_at=created_at, id__lt=item_id))
        items = list(queryset.order_by("-featured", "-created_at", "-id")[: limit + 1])
        has_next = len(items) > limit
        items = items[:limit]
        data = [{"id": item.id, "title": item.title, "slug": item.slug, "description": item.description, "category": item.category, "techStack": item.tech_stack, "imageUrl": item.image_url, "projectUrl": item.project_url, "githubUrl": item.github_url, "featured": item.featured} for item in items]
        return JsonResponse({"data": data, "pagination": {"nextCursor": _cursor_encode(items[-1]) if has_next else None}})


class BlogListView(View):
    def get(self, request):
        limit = _page_size(request)
        queryset = BlogPost.objects.only("id", "title", "slug", "content", "excerpt", "tags", "published_at", "views_count").filter(published_at__isnull=False, published_at__lte=timezone.now())
        cursor = _blog_cursor_decode(request.GET.get("cursor", "")) if request.GET.get("cursor") else None
        if request.GET.get("cursor") and cursor is None:
            return _error("Invalid pagination cursor.")
        if cursor:
            published_at, item_id = cursor
            queryset = queryset.filter(Q(published_at__lt=published_at) | Q(published_at=published_at, id__lt=item_id))
        items = list(queryset.order_by("-published_at", "-id")[: limit + 1])
        has_next = len(items) > limit
        items = items[:limit]
        data = [{"id": item.id, "title": item.title, "slug": item.slug, "content": item.content, "excerpt": item.excerpt, "tags": item.tags, "publishedAt": item.published_at, "viewsCount": item.views_count} for item in items]
        return JsonResponse({"data": data, "pagination": {"nextCursor": _blog_cursor_encode(items[-1]) if has_next else None}}, json_dumps_params={"default": str})


class SkillListView(View):
    def get(self, request):
        items = Skill.objects.only("id", "name", "category", "proficiency_level").order_by("category", "-proficiency_level", "name")
        return JsonResponse({"data": [{"id": item.id, "name": item.name, "category": item.category, "proficiencyLevel": item.proficiency_level} for item in items]})


class ContactSubmissionView(View):
    def post(self, request):
        ip = _client_ip(request)
        key = f"contact-submit:{ip or 'unknown'}"
        if not cache.add(key, 1, 900):
            try:
                count = cache.incr(key)
            except ValueError:
                count = 2
            if count > 8:
                return JsonResponse({"error": {"code": "RATE_LIMITED", "message": "Too many messages. Try again later."}}, status=429)
        try:
            payload = json.loads(request.body or "{}")
        except json.JSONDecodeError:
            return _error("Request body must be valid JSON.")
        form = ContactSubmissionForm(data={
            "name": payload.get("name", ""),
            "email": payload.get("email", ""),
            "subject": payload.get("subject", ""),
            "message_body": payload.get("message", ""),
        })
        if not form.is_valid():
            return _error("Please provide a valid name, email, subject and message.")
        with transaction.atomic():
            submission = form.save(commit=False)
            submission.ip_address = ip
            submission.user_agent = request.META.get("HTTP_USER_AGENT", "")[:500]
            submission.save()
        return JsonResponse({"data": {"id": submission.id, "createdAt": submission.submitted_at}}, status=201, json_dumps_params={"default": str})


class VisitLogView(View):
    def post(self, request):
        try:
            payload = json.loads(request.body or "{}")
        except json.JSONDecodeError:
            return _error("Request body must be valid JSON.")
        page = str(payload.get("pageVisited", "/")).strip()[:500] or "/"
        referrer = str(payload.get("referrer", "")).strip()[:500]
        HighVolumeLogEntry.objects.create(action_category="page_view", description=page, visitor_ip=_client_ip(request), metadata={"referrer": referrer, "user_agent": request.META.get("HTTP_USER_AGENT", "")[:500]})
        return JsonResponse({"data": {"accepted": True}}, status=202)
