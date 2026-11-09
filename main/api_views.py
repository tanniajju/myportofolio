from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import (
    api_view, authentication_classes, permission_classes,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from main.models import Project, Experience, Skill
from main.permissions import IsPortfolioOwnerOrReadOnly, IsPortfolioOwnerOrEditorOrReadOnly
from main.serializers import ProjectSerializer, ExperienceSerializer, SkillSerializer

# shared helpers
def _list_response(request, queryset, serializer_class):
    if request.method in ("GET", "HEAD"):
        serializer = serializer_class(
            queryset, many=True, context={"request": request}
        )
        return Response(serializer.data)

    serializer = serializer_class(data=request.data, context={"request": request})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)

def _detail_response(request, instance, serializer_class):
    if request.method in ("GET", "HEAD"):
        return Response(serializer_class(instance, context={"request": request}).data)
    
    if request.method == "DELETE":
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    serializer = serializer_class(
        instance, data=request.data, partial=request.method == "PATCH",
        context={"request": request},
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)

def _toggle_star_response(request, instance, serializer_class):
    if instance.starred_by.filter(pk=request.user.pk).exists():
        instance.starred_by.remove(request.user)
    else:
        instance.starred_by.add(request.user)
    return Response(serializer_class(instance, context={"request": request}).data)

# project (owner only)
@api_view(["GET", "HEAD", "POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrReadOnly])
def project_list(request):
        projects = Project.objects.prefetch_related("starred_by").order_by("title", "id")
        title = request.query_params.get("title", "").strip()
        if title:
            projects = projects.filter(title__icontains=title)
        return _list_response(request, projects, ProjectSerializer)

@api_view(["GET", "HEAD", "PUT", "PATCH", "DELETE"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrReadOnly])
def project_detail(request, project_id):
    project = get_object_or_404(
        Project.objects.prefetch_related("starred_by"), pk=project_id,
    )
    return _detail_response(request, project, ProjectSerializer)

@api_view(["POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def project_star(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    return _toggle_star_response(request, project, ProjectSerializer)

# skill (owner and editor)
@api_view(["GET", "HEAD", "POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def skill_list(request):
    skills = Skill.objects.prefetch_related("starred_by").order_by("category", "name", "id")
    name = request.query_params.get("name", "").strip()
    if name:
        skills = skills.filter(name__icontains=name)
    return _list_response(request, skills, SkillSerializer)

@api_view(["GET", "HEAD", "PUT", "PATCH", "DELETE"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def skill_detail(request, skill_id):
    skill = get_object_or_404(Skill.objects.prefetch_related("starred_by"), pk=skill_id)
    return _detail_response(request, skill, SkillSerializer)

@api_view(["POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def skill_star(request, skill_id):
    skill = get_object_or_404(Skill, pk=skill_id)
    return _toggle_star_response(request, skill, SkillSerializer)

# experience (owner and editor)
@api_view(["GET", "HEAD", "POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def experience_list(request):
    experiences = Experience.objects.prefetch_related("starred_by").order_by(
        "-started_at", "title", "id",)
    title = request.query_params.get("title", "").strip()
    if title:
        experiences = experiences.filter(title__icontains=title)
    return _list_response(request, experiences, ExperienceSerializer)

@api_view(["GET", "HEAD", "PUT", "PATCH", "DELETE"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def experience_detail(request, experience_id):
    experience = get_object_or_404(Experience.objects.prefetch_related("starred_by"), pk=experience_id)
    return _detail_response(request, experience, ExperienceSerializer)

@api_view(["POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def experience_star(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)
    return _toggle_star_response(request, experience, ExperienceSerializer)
