from rest_framework import serializers

from core.models import School, Course, Administrator, Teacher, Student


class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = ["name", "address"]


class AdministratorSerializer(serializers.ModelSerializer):
    school_id = serializers.IntegerField(source="school.id")
    class Meta:
        model = Administrator
        fields = ["name", "school_id"]

    def create(self, validated_data):
        school_data = validated_data.pop("school")
        try:
            school = School.objects.get(id=school_data.get("id"))
            admin = Administrator.objects.create(school=school, **validated_data)
            return admin
        except School.DoesNotExist:
            raise serializers.ValidationError("Invalid data for School")

    def update(self, instance, validated_data):
        school_data = validated_data.pop("school")
        try:
            school = School.objects.get(id=school_data.get("id"))
            instance.school = school
            instance.name = validated_data.get("name")
            instance.save()
            return instance
        except School.DoesNotExist:
            raise serializers.ValidationError("Invalid data for School")


class TeacherSerializer(serializers.ModelSerializer):
    school_id = serializers.IntegerField(source="school.id")
    class Meta:
        model = Teacher
        fields = ["name", "school_id"]

    def create(self, validated_data):
        school_data = validated_data.pop("school")
        try:
            school = School.objects.get(id=school_data.get("id"))
            teacher = Teacher.objects.create(school=school, **validated_data)
            return teacher
        except School.DoesNotExist:
            raise serializers.ValidationError("Invalid data for School")

    def update(self, instance, validated_data):
        school_data = validated_data.pop("school")
        try:
            school = School.objects.get(id=school_data.get("id"))
            instance.school = school
            instance.name = validated_data.get("name")
            instance.save()
            return instance
        except School.DoesNotExist:
            raise serializers.ValidationError("Invalid data for School")

class CourseSerializer(serializers.ModelSerializer):
    school_id = serializers.IntegerField(source="school.id")
    teacher_id = serializers.IntegerField(source="teacher.id")
    class Meta:
        model = Course
        fields = ["name", "location", "school_id", "teacher_id"]

    def create(self, validated_data):
        school_data = validated_data.pop("school")
        teacher_data = validated_data.pop("teacher")
        try:
            school = School.objects.get(id=school_data.get("id"))
            teacher = Teacher.objects.get(id=teacher_data.get("id"))
            course = Course.objects.create(school=school, teacher=teacher, **validated_data)
            return course
        except School.DoesNotExist:
            raise serializers.ValidationError("Invalid data for School")
        except Teacher.DoesNotExist:
            raise serializers.ValidationError("Invalid data for Teacher")

    def update(self, instance, validated_data):
        school_data = validated_data.pop("school")
        teacher_data = validated_data.pop("teacher")
        try:
            school = School.objects.get(id=school_data.get("id"))
            teacher = Teacher.objects.get(id=teacher_data.get("id"))
            instance.school = school
            instance.teacher = teacher
            instance.name = validated_data.get("name")
            instance.location = validated_data.get("location")
            instance.save()
            return instance
        except School.DoesNotExist:
            raise serializers.ValidationError("Invalid data for School")
        except Teacher.DoesNotExist:
            raise serializers.ValidationError("Invalid data for Teacher")


class StudentSerializer(serializers.ModelSerializer):
    school_id = serializers.IntegerField(source="school.id")
    course_id = serializers.IntegerField(source="course.id")
    class Meta:
        model = Student
        fields = ["name", "school_id", "course_id"]

    def create(self, validated_data):
        school_data = validated_data.pop("school")
        course_data = validated_data.pop("course")
        try:
            school = School.objects.get(id=school_data.get("id"))
            course = Course.objects.get(id=course_data.get("id"))
            student = Student.objects.create(school=school, course=course, **validated_data)
            return student
        except School.DoesNotExist:
            raise serializers.ValidationError("Invalid data for School")
        except Course.DoesNotExist:
            raise serializers.ValidationError("Invalid data for Course")

    def update(self, instance, validated_data):
        school_data = validated_data.pop("school")
        course_data = validated_data.pop("course")
        try:
            school = School.objects.get(id=school_data.get("id"))
            course = Course.objects.get(id=course_data.get("id"))
            instance.school = school
            instance.course = course
            instance.name = validated_data.get("name")
            instance.save()
            return instance
        except School.DoesNotExist:
            raise serializers.ValidationError("Invalid data for School")
        except Course.DoesNotExist:
            raise serializers.ValidationError("Invalid data for Course")
