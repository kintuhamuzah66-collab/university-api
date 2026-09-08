
from django.shortcuts import render, redirect
from django.http import HttpResponse
from students.models import Student
from departments.models import Department
from students.forms import StudentForm, StudentModelForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

@login_required
def student_list(request):
    print("USER:", request.user)
    print("AUTHENTICATED:", request.user.is_authenticated)
    students = Student.objects.all()
    total_students = Student.objects.count()

    output = ""

    for student in students:
        output += f"{student.firstname} {student.surname}<br>"

    return render(
        request,
        "students/student_list.html",
        {
            "title": "Student Management System", 
            "students": students
        }
    )


"""
from django.views.generic import ListView

class StudentListView(ListView):
    model = Student
    template_name = "students/list.html"
    context_object_name = "students"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Student Management System"
        context["total"] = Student.objects.count()
        return context
"""
@login_required
def student_detail(request, id):
    if not request.user.has_perm("students.view_student"):
        return HttpResponseForbidden(
            "You do not have permission to view students"
        )
    student = Student.objects.get(id=id)
    return render(
        request,
        "students/detail.html",
        {
            "student": student
        }
    )



def create_student(request):

    if request.method == "POST":

        firstname = request.POST.get("firstname")
        surname = request.POST.get("surname")
        email = request.POST.get("email")
        dob = request.POST.get("date_of_birth")

        department = Department.objects.get(
            id=request.POST.get("department")
        )

        Student.objects.create(
            firstname=firstname,
            surname=surname,
            email=email,
            date_of_birth=dob,
            department=department
        )

        return redirect("student_list")

    departments = Department.objects.all()

    return render(
        request,
        "students/create.html",
        {
            "departments": departments
        }
    )


def register_student(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            firstname = form.cleaned_data['firstname']
            surname = form.cleaned_data['surname']
            email = form.cleaned_data['email']
            print(f"{firstname} {surname} email: {email}")
    else:
        form = StudentForm()
    
    return render(
        request,
        "students/register.html",
        {
            "form": form
        }
    )

def student_create(request):
    if request.method == "POST":
        form = StudentModelForm(
            request.POST,
            request.FILES
        )
        if form.is_valid():
            student = form.save(commit=False)
            student.full_name = (
                f"{student.firstname} {student.surname}"
            )
            student.save()
            return redirect("student_create")
    else:
        form = StudentModelForm()
    return render(
        request,
        "students/student_create.html",
        {
            "form": form
        }
    )


def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )
        if user is not None:
            login(request, user)
            return redirect("student_list")
    return render(
        request,
        "students/login.html"
    )

def logout_user(request):
    logout(request)

    return redirect("login")
