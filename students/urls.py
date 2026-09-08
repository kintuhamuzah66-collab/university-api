from django.urls import path 
from . import views

urlpatterns = [
    path("", views.student_list, name="student_list"),
    path("<int:id>/",
        views.student_detail,
        name="student_detail"
    ),
    path(
        "create/",
        views.create_student,
        name="create_student"
    ),
    path(
        "register/",
        views.register_student,
        name="register_student"
    ),
    path(
        "create_new_student/",
        views.student_create,
        name="student_create"
    ),
    #path("", views.StudentListView.as_view()),
    path(
        "login/",
        views.user_login,
        name="login"
    ),
    path(
        "logout/",
        views.logout_user,
        name="logout"
    ),

]