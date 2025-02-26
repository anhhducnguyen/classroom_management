# from django.contrib import admin
# from .models import Enrollment, Student, StudentHistory, Teacher, Class

# @admin.register(Student)
# class StudentAdmin(admin.ModelAdmin):
#     list_display = ('full_name', 'student_code', 'birth_date', 'current_school')
#     search_fields = ('full_name', 'student_code')
#     ordering = ('student_code',)

# @admin.register(Teacher)
# class TeacherAdmin(admin.ModelAdmin):
#     list_display = ('full_name', 'teacher_code', 'birth_date', 'current_school')
#     search_fields = ('full_name', 'teacher_code')
#     ordering = ('teacher_code',)

# @admin.register(Class)
# class ClassAdmin(admin.ModelAdmin):
#     list_display = ('class_name', 'start_date', 'end_date', 'teacher')
#     search_fields = ('class_name',)
#     list_filter = ('start_date', 'end_date')

# @admin.register(Enrollment)
# class EnrollmentAdmin(admin.ModelAdmin):
#     list_display = ('student', 'class_enrolled', 'status', 'enrollment_date')
#     list_filter = ('status', 'class_enrolled')
#     search_fields = ('student__full_name', 'class_enrolled__class_name')

# @admin.register(StudentHistory)
# class StudentHistoryAdmin(admin.ModelAdmin):
#     list_display = ('student', 'previous_class', 'action', 'date')
#     list_filter = ('action', 'date')


from django.contrib import admin
from django.contrib.auth.models import User
from .models import StudentUser, Class, Schedule

# Đăng ký StudentUser
@admin.register(StudentUser)
class StudentUserAdmin(admin.ModelAdmin):
    list_display = ("full_name", "student_code", "birth_date", "current_school")
    search_fields = ("full_name", "student_code", "current_school")
    list_filter = ("current_school",)

# Đăng ký Class
@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ("class_name", "teacher_display", "student_count")
    search_fields = ("class_name",)
    list_filter = ("teacher",)
    
    def teacher_display(self, obj):
        return obj.teacher.username if obj.teacher else "Chưa có giáo viên"
    teacher_display.short_description = "Giáo viên"

    def student_count(self, obj):
        return obj.students.count()
    student_count.short_description = "Số học viên"

# Đăng ký Schedule
@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ("class_assigned", "teacher", "day_of_week", "session", "start_time", "end_time", "room")
    search_fields = ("class_assigned__class_name", "teacher__username")
    list_filter = ("day_of_week", "session", "teacher")


