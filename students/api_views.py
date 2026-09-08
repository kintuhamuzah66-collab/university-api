"""
from rest_framework.response import Response
from rest_framework.decorators import api_view
from students.serializers import StudentSerializer, GetStudentSerializer
from students.models import Student


@api_view(["GET", "POST"])
def student_api(request):
    if request.method == "GET":
        students = Student.objects.all()

        serializer = GetStudentSerializer(students, many=True)
    
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = StudentSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
                serializer.data
            )

"""

from rest_framework import generics, viewsets
from students.models import Student
from students.serializers import StudentSerializer
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .permissions import IsStaffOrReadOnly

class StudentListCreateView(generics.ListCreateAPIView):
    #queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def get_queryset(self):
        return Student.objects.filter(is_active=True)

class StudentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]


###################################
# class based views using APIView #
###################################


from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status

class StudentAPIView(APIView):
    def get(self, request):
        students = Student.objects.all()

        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = StudentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)

class StudentDetailAPIView(APIView):
    def delete(self, request, pk):
        student = get_object_or_404(Student, pk=pk)
        student.delete()
        return Response(status=204)

    def get(self, request, pk):
        student = get_object_or_404(Student,pk=pk)
        serializer = StudentSerializer(student)
        return Response(serializer.data)

    def patch(self, request, pk):
        student = get_object_or_404(Student, pk=pk)
        serializer = StudentSerializer(
            student,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status = status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status = status.HTTP_400_BAD_REQUEST
        )
