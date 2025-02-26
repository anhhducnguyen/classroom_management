from rest_framework import viewsets
from django.contrib.auth.models import User
from .models import StudentUser, Class, Schedule
from .serializers import StudentUserSerializer, ClassSerializer, ScheduleSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.shortcuts import render


class StudentUserViewSet(viewsets.ModelViewSet):
    """
    API CRUD cho StudentUser (Học viên)
    """
    queryset = StudentUser.objects.all()
    serializer_class = StudentUserSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class ClassViewSet(viewsets.ModelViewSet):
    """
    API CRUD cho Class (Lớp học)
    """
    queryset = Class.objects.all()
    serializer_class = ClassSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class ScheduleViewSet(viewsets.ModelViewSet):
    """
    API CRUD cho Schedule (Thời khóa biểu)
    """
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

def test_static(request):
    return render(request, 'index.html')

from django.http import JsonResponse

def schedule_list(request):
    schedules = Schedule.objects.all().values(
        "class_assigned__name", "teacher__name", "day_of_week",
        "session", "start_time", "end_time", "room"
    )
    return JsonResponse(list(schedules), safe=False)

