from django.forms import ModelForm, TextInput, Textarea, URLInput, Select, NumberInput
from main.models import Project, Skill

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = [
            "title",
            "description",
            "tech_stack",
            "project_url",
            "project_image_url",
        ]

        labels = {
            "title": "Nama Proyek",
            "description": "Deskripsi Proyek",
            "tech_stack": "Teknologi yang Digunakan",
            "project_url": "URL Proyek",
            "project_image_url": "URL Gambar Proyek",
        }

        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "Portfolio Website",
                    "maxlength": 255,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Ceritakan Tentang Proyekmu",
                    "rows": 3,
                }
            ),
            "tech_stack": TextInput(
                attrs={
                    "placeholder": "Django, Python, HTML, CSS",
                }
            ),
            "project_url": URLInput(
                attrs={
                    "placeholder": "https://github.com/kakBurhan/burhanquestv4",
                }
            ),
            "project_image_url": URLInput(
                attrs={
                    "placeholder": "https://drive.google.com/thumbnail?id=...&sz=w1000",
                }
            ),
        }

class SkillForm(ModelForm):
    class Meta:
        model = Skill
        fields = [
            "name",
            "description",
            "category",
            "nilai",
            "skill_image_url",
        ]

        labels = {
            "name": "Nama skill",
            "description": "Deskripsi skill",
            "category": "Kategori skill",
            "nilai": "Tingkat keahlian dalam skala 1-100",
            "skill_image_url": "URL gambar terkait skill",
        }

        widgets = {
            "name": TextInput(
                attrs={
                    "placeholder": "Python",
                    "maxlength": 100,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Ceritakan Tentang Skillmu",
                    "rows": 3,
                }
            ),
            "category": Select(
                attrs={'class': 'form-select'}
            ),
            "nilai": NumberInput(attrs={
                "type": "range",               
                "class": "form-range",         
                "min": "1",
                "max": "100",
                "step": "5",                   
            }),
            "skill_image_url": URLInput(
                attrs={
                    "placeholder": "https://drive.google.com/thumbnail?id=...&sz=w1000",
                }
            ),
        }