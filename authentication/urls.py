from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudentUserViewSet, ClassViewSet, ScheduleViewSet
from . import views

router = DefaultRouter()
router.register(r'students', StudentUserViewSet, basename="studentuser")
router.register(r'classes', ClassViewSet, basename="class")
router.register(r'schedules', ScheduleViewSet, basename="schedule")

urlpatterns = [
    path('api/', include(router.urls)), 
    path('', views.test_static, name='home'),
    path("api/schedules/", views.schedule_list, name="schedule_list"),
    path(
    "google_sso/", include("django_google_sso.urls", namespace="django_google_sso")
    ),
]
