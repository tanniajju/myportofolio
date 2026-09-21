from django.urls import path
from main.views import show_main, show_experience, show_skill, create_project, show_project, get_projects_json, delete_project, create_skill, get_skills_json, delete_skill

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("experience/", show_experience, name="show_experience"),
    path("skill/", show_skill, name="show_skill"),
    path("skill/add/", create_skill, name="create_skill"),
    path("api/skill/", get_skills_json, name="get_projects_json"),
    path('delete_skill/<uuid:skill_id>/', delete_skill, name='delete_skill'),
    path("project", show_project, name="show_project"),
    path("project/add/", create_project, name="create_project"),
    path("api/project/", get_projects_json, name="get_projects_json"),
    path("projects/<uuid:project_id>/delete/",delete_project,name="delete_project"),
]