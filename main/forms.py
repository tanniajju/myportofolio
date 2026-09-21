from django.forms import ModelForm, TextInput, Textarea, URLInput, Select, NumberInput, DateInput, ChoiceField
from main.models import Experience, Project, Skill

class ExperienceForm(ModelForm):
    category = ChoiceField(
        choices=[('', '--- Pilih kategori ---')] + Experience.EXPERIENCE_CHOICES,
        widget=Select(attrs={'class': 'form-select'})
    )
    class Meta:
        model = Experience
        fields = [
            "title",
            "description",
            "category",
            "thumbnail",
            "started_at",
            "ended_at"
        ]

        labels = {
            "title": "Nama pengalaman",
            "description": "Deskripsi pengalaman",
            "category": "Kategori pengalaman",
            "thumbnail": "URL gambar terkait pengalaman",
            "started_at": "Waktu pengalaman dimulai",
            "ended_at": "Waktu pengalaman selesai",
        }

        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "Staff Acara Project Kesenian",
                    "maxlength": 255,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Ceritakan Tentang Skillmu",
                    "rows": 3,
                }
            ),
            "thumbnail": URLInput(
                attrs={
                    "placeholder": "https://drive.google.com/thumbnail?id=...&sz=w1000",
                }
            ),
            'started_at': DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control',
                }
            ),
            'ended_at': DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control',
                }
            ),
        }

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
    category = ChoiceField(
        choices=[('', '--- Pilih kategori ---')] + Skill.SKILL_CHOICES,
        widget=Select(attrs={'class': 'form-select'})
    )

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