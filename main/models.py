import uuid
from django.db import models

class Experience(models.Model):
    EXPERIENCE_CHOICES = [
        ('internship', 'Internship'),
        ('research', 'Research'),
        ('volunteer', 'Volunteer'),
        ('part-time', 'Part-Time'),
        ('full-time', 'Full-Time'),
        ('freelance', 'Freelance'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES, default='full-time')
    thumbnail = models.URLField(blank=True, null=True)
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(blank=True, null=True)
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

    LEVEL_CHOICES = [
        ('familiar', 'Familiar'),
        ('proficient', 'Proficient'),
        ('advanced', 'Advanced'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=SKILL_CHOICES, default='tools')
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='proficient')
    image_path = models.CharField(max_length=255, blank=True, null=True)
    def __str__(self):
        return self.name