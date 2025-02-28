from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudentUserViewSet, ClassViewSet, ScheduleViewSet
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

from . import views

router = DefaultRouter()
router.register(r'students', StudentUserViewSet, basename="studentuser")
router.register(r'classes', ClassViewSet, basename="class")

urlpatterns = [
    path('api/', include(router.urls)), 
    path('', views.home, name='home'),
    path('home', views.home_page, name='home_page'),
    path("api/schedules/student/", views.ScheduleViewSet.as_view({'get': 'student_schedule'}), name="student_schedule"),

    # Signup, Sign in, Sign out and activate account
    path('signup', views.signup, name='signup'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('signin', views.signin, name='signin'),
    path('signout', views.signout, name='signout'),

    path(
    "google_sso/", include("django_google_sso.urls", namespace="django_google_sso")
    ),

    # Forgot password
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset_form.html'), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
