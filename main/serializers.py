from django.utils.html import strip_tags
from rest_framework import serializers

from main.models import Project, Skill, Experience

STAR_FIELDS = ["star_count", "is_starred", "starred_by_names"]

def clean_text(value, label):
    cleaned = strip_tags(value).strip()
    if not cleaned:
        raise serializers.ValidationError(f"{label} cannot be empty.")
    return cleaned

class StarredModelSerializer(serializers.ModelSerializer):
    star_count = serializers.SerializerMethodField()
    is_starred = serializers.SerializerMethodField()
    starred_by_names = serializers.SerializerMethodField()

    def get_star_count(self, obj):
        return obj.starred_by.count()

    def get_is_starred(self, obj):
        request = self.context.get("request")
        if request is None or not request.user.is_authenticated:
            return False
        return request.user in obj.starred_by.all()

    def get_starred_by_names(self, obj):
        return ", ".join(user.username for user in obj.starred_by.all())

class ProjectSerializer(StarredModelSerializer):
    class Meta:
        model = Project
        fields = [
            "id", "title", "description", "tech_stack",
            "project_url", "project_image_url",
            *STAR_FIELDS,
        ]
        read_only_fields = ["id"]

    def validate_title(self, value):
        return clean_text(value, "Title")

    def validate_description(self, value):
        return clean_text(value, "Description")

    def validate_tech_stack(self, value):
        return clean_text(value, "Tech Stack")

class SkillSerializer(StarredModelSerializer):
    category_display = serializers.CharField(source="get_category_display", read_only=True)

    class Meta:
        model = Skill
        fields = ["id", "name", "description", "category", "category_display",
                  "nilai", "skill_image_url", *STAR_FIELDS]
        read_only_fields = ["id"]

    def validate_name(self, value):
        return clean_text(value, "Name")

    def validate_description(self, value):
        return clean_text(value, "Description")

class ExperienceSerializer(StarredModelSerializer):
    is_ongoing = serializers.BooleanField(read_only=True)

    class Meta:
        model = Experience
        fields = ["id", "title", "description", "category", "thumbnail",
                  "started_at", "ended_at", "is_ongoing", *STAR_FIELDS]
        read_only_fields = ["id"]
        extra_kwargs = {"started_at": {"required": True}}

    def validate_title(self, value):
        return clean_text(value, "Title")

    def validate_description(self, value):
        return clean_text(value, "Description")

    def validate(self, attrs):
        if "started_at" not in attrs and "ended_at" not in attrs:
            return attrs
        started_at = attrs["started_at"] if "started_at" in attrs else self.instance.started_at
        ended_at = attrs["ended_at"] if "ended_at" in attrs else (
            self.instance.ended_at if self.instance else None)
        if ended_at is not None and ended_at < started_at:
            raise serializers.ValidationError(
                {"ended_at": "End date cannot be earlier than the start date."})
        return attrs