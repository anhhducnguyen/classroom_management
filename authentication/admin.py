import random
from django.contrib import admin
from django.contrib.auth.models import User
from .models import StudentUser, Class, Schedule
from unfold import admin as unfold_admin
from django.contrib.auth.models import User, Group  
from unfold.decorators import action, display
from authentication.sites import authentication_admin_site
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.utils.timezone import now, timedelta
from unfold.components import BaseComponent, register_component
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




@register_component
class CohortComponent(BaseComponent):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        rows = []
        headers = []
        cols = []

        dates = reversed(
            [(now() - timedelta(days=x)).strftime("%B %d, %Y") for x in range(8)]
        )
        groups = range(1, 10)

        for row_index, date in enumerate(dates):
            cols = []

            for col_index, _col in enumerate(groups):
                color_index = 8 - row_index - col_index
                col_classes = []

                if color_index > 0:
                    col_classes.append(
                        f"bg-primary-{color_index}00 dark:bg-primary-{9 - color_index}00"
                    )

                if color_index >= 4:
                    col_classes.append("text-white dark:text-gray-600")

                value = random.randint(
                    4000 - (col_index * row_index * 225),
                    5000 - (col_index * row_index * 225),
                )

                subtitle = f"{random.randint(10, 100)}%"

                if value <= 0:
                    value = 0
                    subtitle = None

                cols.append(
                    {
                        "value": value,
                        "color": " ".join(col_classes),
                        "subtitle": subtitle,
                    }
                )

            rows.append(
                {
                    "header": {
                        "title": date,
                        "subtitle": f"Total {sum(col['value'] for col in cols):,}",
                    },
                    "cols": cols,
                }
            )

        for index, group in enumerate(groups):
            total = sum(row["cols"][index]["value"] for row in rows)

            headers.append(
                {
                    "title": f"Group #{group}",
                    "subtitle": f"Total {total:,}",
                }
            )
        context["data"] = {
            "headers": headers,
            "rows": rows,
        }
        return context
    
@register_component
class TrackerComponent(BaseComponent):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data = []

        for i in range(1, 72):
            has_value = random.choice([True, True, True, True, False])
            color = None
            tooltip = None
            if has_value:
                value = random.randint(2, 6)
                color = f"bg-primary-{value}00 dark:bg-primary-{9 - value}00"
                tooltip = f"Value {value}"

            data.append(
                {
                    "color": color,
                    "tooltip": tooltip,
                }
            )

        context["data"] = data
        return context


admin.site.unregister(User)  
admin.site.unregister(Group)  

admin.site.register(User, CustomUserAdmin)  
admin.site.register(Group, CustomGroupAdmin) 


