from django.shortcuts import render
from main.models import Experience, Skill


def show_main(request):
    context = {
        "name": "Tania Ju",
        "npm": "2506608123",
        "study_program": "S1 Sistem Informasi",
        "bio": (
            "Mahasiswa Sistem Informasi Universitas Indonesia yang tertarik "
            "pada pengembangan perangkat lunak dan pendidikan."
        ),
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Tania Ju",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)

def show_skill(request):
    context = { 
        'languages': Skill.objects.filter(category="languages"),
        'frameworks': Skill.objects.filter(category="frameworks"),
        'tools':Skill.objects.filter(category='tools'),
    }
    return render(request, "skill.html", context)