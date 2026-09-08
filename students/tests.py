from django.test import TestCase 
from .models import Student
from departments.models import Department

class StudentTestCase(TestCase):
    fixtures = ["students_fixture.json"]

    def test_student_list_requires_authentication(self):
        response = self.client.get("/api/students/")
        self.assertEqual(response.status_code, 401)

        self.assertEqual(response.json()["detail"], "Authentication credentials were not provided.")

    def test_students_exist(self):
        self.assertGreater(Student.objects.count(), 0)

from django.db.models import ProtectedError
class StudentModelTest(TestCase):

    def test_student_can_be_created(self):
        department = Department.objects.create(
            name="Computer Science"
        )

        student = Student.objects.create(
            surname="Kintu",
            firstname="Hamza",
            email="hamza@example.com",
            date_of_birth="2002-07-12",
            department=department
        )

        self.assertEqual(Student.objects.count(), 1)
        self.assertEqual(student.firstname, "Hamza")
        self.assertEqual(student.surname, "Kintu")
        self.assertEqual(student.email, "hamza@example.com")

    def test_student_is_active_by_default(self):
        department = Department(
            name = "Software Engineering"
        )

        student = Student(
            surname="Nakintu",
            firstname="Aidah",
            email="naki@example.com",
            date_of_birth="2002-07-12",
            department=department
        )

        self.assertEqual(student.is_active, True)

    def test_string_for_full_name(self):
        department = Department.objects.create(
                    name = "Software Engineering"
                )
        student = Student.objects.create(
                    surname="Nakintu",
                    firstname="Aidah",
                    email="naki@example.com",
                    date_of_birth="2002-07-12",
                    department=department
                )
        self.assertEqual(str(student), "Aidah Nakintu")

    def test_student_belongs_to_department(self):
        department = Department.objects.create(
                            name = "Software Engineering"
                        )
        student = Student.objects.create(
                            surname="Nakintu",
                            firstname="Aidah",
                            email="naki@example.com",
                            date_of_birth="2002-07-12",
                            department=department
                        )
        student = Student.objects.create(
                            surname="Kaliro",
                            firstname="Aidah",
                            email="Kaliro@example.com",
                            date_of_birth="2002-07-12",
                            department=department
                        )
                
        self.assertEqual(student.department, department)
        self.assertEqual(department.students.count(), 2)


    def test_deleting_a_department(self):

        department = Department.objects.create(
            name="Computer Science"
        )

        student = Student.objects.create(
                                    surname="Kaliro",
                                    firstname="Aidah",
                                    email="Kaliro@example.com",
                                    date_of_birth="2002-07-12",
                                    department=department
                                )
        self.assertRaises(
            ProtectedError,
            department.delete
        )



#######################################################################
#       TESTING SERIALIZERS                                           #
#######################################################################
from students.serializers import StudentSerializer

class StudentSerializerTest(TestCase):
    def test_valid_student_data(self):

        department = Department.objects.create(
            name="Computer Science"
        )

        data = {
            "surname": "Kintu",
            "firstname": "Hamza",
            "email": "hamza@example.com",
            "date_of_birth": "2002-07-12",
            "department": department.id
        }

        serializer = StudentSerializer(data=data)
        # self.assertEqual(serializer.is_valid(), False)
        self.assertTrue(serializer.is_valid())  # this one is better

    def test_missing_surname_is_invalid(self):
        department = Department.objects.create(
            name="Computer Science"
        )

        data = {
            "firstname": "Hamza",
            "email": "hamza@example.com",
            "date_of_birth": "2002-07-12",
            "department": department.id
        }

        serializer = StudentSerializer(data=data)
        self.assertFalse(serializer.is_valid())

        print(serializer.errors)      # tells us what the errors  are

    def test_student_is_serialized(self):
        department = Department.objects.create(
            name="Computer Science"
        )

        student = Student.objects.create(
            surname="Kintu",
            firstname="Hamza",
            email="hamza@example.com",
            date_of_birth="2002-07-12",
            department=department
        )

        serializer = StudentSerializer(student)

        self.assertEqual(serializer.data["firstname"], "Hamza")
        self.assertEqual(serializer.data["surname"], "Kintu")
        self.assertEqual(serializer.data["email"], "hamza@example.com")




##########################################################################
###       Testing the api endpoint                                  ######
##########################################################################

from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APIClient

class StudentAPITest(TestCase):

    def test_get_student(self):
        department = Department.objects.create(
            name="Computer Science"
        )

        student = Student.objects.create(
            surname="Kintu",
            firstname="Hamza",
            email="hamza@example.com",
            date_of_birth="2002-07-12",
            department=department
        )

        response = self.client.get("/api/students/", follow=True)
        self.assertEqual(response.status_code, 401)

    def test_authenticated_user_can_get_students(self):
        User = get_user_model()

        user = User.objects.create_user(
            username="testuser",
            password="password123"
        )

        client = APIClient()

        department = Department.objects.create(
            name="Computer Science"
        )

        Student.objects.create(
            surname="Kintu",
            firstname="Hamza",
            email="hamza@example.com",
            date_of_birth="2002-07-12",
            department=department
        )

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {access_token}"
        )

        response = client.get("/api/students/", follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]["surname"], "Kintu")

    def test_authenticated_user_can_post_a_student(self):
        User = get_user_model()

        user = User.objects.create_user(
            username='testuser',
            password="password123"
        )

        client = APIClient()

        department = Department.objects.create(
            name="Computer Science"
        )
        data = {
            "surname": "Nsubuga",
            "firstname": "John",
            "email": "john@example.com",
            "date_of_birth": "2001-05-20",
            "department": department.id
        }

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {access_token}"
        )

        response = client.post(
            "/api/students/",
            data=data,
            format="json",
            follow=True
        )

        self.assertEqual(response.status_code, 201)
        student = Student.objects.get(email="john@example.com")
        self.assertEqual(student.firstname, "John")