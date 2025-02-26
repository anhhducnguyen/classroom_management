from rest_framework import serializers
from django.contrib.auth.models import User
from .models import StudentUser, Class, Schedule

class StudentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentUser
        fields = ['id', 'full_name', 'address', 'birth_date', 'current_school', 'parent_info', 'student_code']


class ClassSerializer(serializers.ModelSerializer):
    teacher_name = serializers.CharField(source="teacher.username", read_only=True)
    students = StudentUserSerializer(many=True, read_only=True)

    class Meta:
        model = Class
        fields = ['id', 'class_name', 'teacher', 'teacher_name', 'students']


class ScheduleSerializer(serializers.ModelSerializer):
    class_assigned_name = serializers.CharField(source="class_assigned.class_name", read_only=True)
    teacher_name = serializers.CharField(source="teacher.username", read_only=True)
    day_of_week_display = serializers.CharField(source="get_day_of_week_display", read_only=True)
    session_display = serializers.CharField(source="get_session_display", read_only=True)

    class Meta:
        model = Schedule
        fields = [
            'id', 'class_assigned', 'class_assigned_name', 'teacher', 'teacher_name', 
            'day_of_week', 'day_of_week_display', 'session', 'session_display', 
            'start_time', 'end_time', 'room'
        ]
