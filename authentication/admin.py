from django.contrib import admin
from django.contrib.auth.models import User
from .models import StudentUser, Class, Schedule
from unfold import admin as unfold_admin
from django.contrib.auth.models import User, Group  
from unfold.decorators import action, display
from authentication.sites import authentication_admin_site
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from unfold.admin import ModelAdmin
from unfold.contrib.filters.admin import (
    ChoicesDropdownFilter,
    RangeDateFilter,
    RangeNumericFilter,
    SingleNumericFilter,
    TextFilter,
)
from django.core.validators import EMPTY_VALUES

@admin.register(StudentUser)
class StudentUserAdmin(unfold_admin.ModelAdmin):
    list_display = ("full_name", "student_code", "birth_date", "current_school")
    search_fields = ("full_name", "student_code", "current_school")
    list_filter = ("current_school", "birth_date", "full_name")

@admin.register(Class)
class ClassAdmin(unfold_admin.ModelAdmin):
    list_display = ("class_name", "teacher_display", "student_count")
    search_fields = ("class_name",)
    list_filter = ("teacher",)
    
    def teacher_display(self, obj):
        return obj.teacher.username if obj.teacher else "Chưa có giáo viên"
    teacher_display.short_description = "Giáo viên"

    def student_count(self, obj):
        return obj.students.count()
    student_count.short_description = "Số học viên"

@admin.register(Schedule)
class ScheduleAdmin(unfold_admin.ModelAdmin):
    list_display = ("class_assigned", "teacher", "day_of_week", "session", "start_time", "end_time", "room")
    search_fields = ("class_assigned__class_name", "teacher__username")
    list_filter = ("day_of_week", "session", "teacher")

class CustomUserAdmin(ModelAdmin):
    list_display = ('username', 'email', 'date_joined', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ('username', 'email', 'is_active', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email')

    list_filter_submit = True
    list_fullwidth = True

    filter_horizontal = (
        "groups",
        "user_permissions",
    )
   
    readonly_fields = ["last_login", "date_joined"]

    @display(description=("User"))
    def display_header(self, instance: User):
        return instance.username

    @display(description=("Staff"), boolean=True)
    def display_staff(self, instance: User):
        return instance.is_staff

    @display(description=("Superuser"), boolean=True)
    def display_superuser(self, instance: User):
        return instance.is_superuser

    @display(description=("Created"))
    def display_created(self, instance: User):
        return instance.created_at

from unfold.admin import TabularInline


class MyInline(TabularInline):
    model = User
    tab = True
    
@admin.register(Group, site=authentication_admin_site)
class CustomGroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass


admin.site.unregister(User)  
admin.site.unregister(Group)  

admin.site.register(User, CustomUserAdmin)  
admin.site.register(Group, CustomGroupAdmin) 


