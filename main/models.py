import uuid
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class Experience(models.Model):
    EXPERIENCE_CHOICES = [
        ('internship', 'Internship'),
        ('volunteer', 'Volunteer'),
        ('part-time', 'Part-Time'),
        ('full-time', 'Full-Time'),
        ('organization', 'Organization'),
        ('committee', 'Committee')
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES, default='commitee')
    thumbnail = models.URLField(blank=True, null=True)
    started_at = models.DateField(default=timezone.now)
    ended_at = models.DateField(blank=True, null=True)
    def __str__(self):
        return self.title

    @property
    def is_ongoing(self):
        return self.ended_at is None

class Skill(models.Model):
    SKILL_CHOICES = [
        ('languages', 'Programming Language'),
        ('frameworks', 'Frameworks & Libraries'),
        ('tools', 'Tools & Platforms')
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=SKILL_CHOICES, default='tools')
    nilai = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)], default=50)
    skill_image_url = models.URLField(blank=True, max_length=500)
    def __str__(self):
        return self.name


class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    tech_stack = models.CharField(max_length=255)
    project_url = models.URLField(blank=True)
    project_image_url = models.URLField(blank=True, max_length=500)

    def __str__(self):
        return self.title