from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404

from core.models import School, Course, Administrator, Teacher, Student
from core.serializers import SchoolSerializer, CourseSerializer, AdministratorSerializer, \
    TeacherSerializer, StudentSerializer


class SchoolViewSet(viewsets.ModelViewSet):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer

    @action(detail=True, methods=['get'])
    def stats(self, request, pk, *args, **kwargs):
        try:
            school = School.objects.get(id=pk)
            result = {
                "id": school.id,
                "courses": Course.objects.filter(school__id=pk).count(),
                "admins": Administrator.objects.filter(school__id=pk).count(),
                "teachers": Teacher.objects.filter(school__id=pk).count(),
                "students": Student.objects.filter(school__id=pk).count()
            }
            return Response(result)
        except School.DoesNotExist:
            raise Http404


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class AdministratorViewSet(viewsets.ModelViewSet):
    queryset = Administrator.objects.all()
    serializer_class = AdministratorSerializer


class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

#
class TransferView(APIView):
    def post(self, request, format=None):
        student_id = request.data.get("studentId")
        from_course_id = int(request.data.get("fromCourseId"))
        to_course_id = int(request.data.get("toCourseId"))
        try:
            student = Student.objects.get(id=student_id)
        except Student.DoesNotExist:
            return Response({"success": False, "message": "Student doest not exist."})

        if student.course_id != from_course_id:
            return Response({"success": False, "message": f"Student isn't included the course {from_course_id}"})

        try:
            course = Course.objects.get(id=to_course_id)
        except Course.DoesNotExist:
            return Response({"success": False, "message": f"Course {to_course_id} does not exist"})

        student.course = course
        student.save()
        return Response({
            "success": True,
            "message": f"Successfully transferred Student {student_id} "
                       f"from Course {from_course_id} to Course {to_course_id}"
        })