from django.urls import path
from main.views import *

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("experience/", show_experience, name="show_experience"),
    path("experience/add/", create_experience, name="create_experience"),
    path("api/experience/", get_experiences_json, name="get_experiences_json"),
    path('delete_experience/<uuid:experience_id>/', delete_experience, name='delete_experience'),
    path("skill/", show_skill, name="show_skill"),
    path("skill/add/", create_skill, name="create_skill"),
    path("api/skill/", get_skills_json, name="get_skills_json"),
    path('delete_skill/<uuid:skill_id>/', delete_skill, name='delete_skill'),
    path("project", show_project, name="show_project"),
    path("project/add/", create_project, name="create_project"),
    path("api/project/", get_projects_json, name="get_projects_json"),
    path("projects/<uuid:project_id>/delete/",delete_project,name="delete_project"),
    path('experience/<uuid:experience_id>/update/', update_experience, name='update_experience'),
    path('skill/<uuid:skill_id>/update/', update_skill, name='update_skill'),
    path('project/<uuid:project_id>/update/', update_project, name='update_project'),
    path("register/", register, name="register"),
    path("login/", login_user, name="login"),
    path("logout/", logout_user, name="logout"),
    path(
        "projects/<uuid:project_id>/star/",
        toggle_star_project,
        name="toggle_star_project",
    ),
    path(
            "experience/<uuid:experience_id>/star/",
            toggle_star_experience,
            name="toggle_star_experience",
        ),
    path(
                "skill/<uuid:skill_id>/star/",
                toggle_star_skill,
                name="toggle_star_skill",
            ),
    path("projects/add-ajax/", create_project_ajax, name="create_project_ajax"),
    ]
    
