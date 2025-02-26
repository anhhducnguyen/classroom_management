# from django.db import models

# class Student(models.Model):
#     full_name = models.CharField("Tên đầy đủ", max_length=255)
#     address = models.TextField("Địa chỉ")
#     birth_date = models.DateField("Ngày sinh")
#     current_school = models.CharField("Trường đang theo học", max_length=255)
#     parent_info = models.TextField("Thông tin phụ huynh")
#     student_code = models.CharField("Mã học viên" ,max_length=10, unique=True, editable=False)

#     def save(self, *args, **kwargs):
#         if not self.student_code:
#             last_student = Student.objects.order_by('-id').first()
#             self.student_code = f"HS{(last_student.id + 1) if last_student else 1:04d}"
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return f"{self.full_name} - {self.student_code}"

# class Teacher(models.Model):
#     full_name = models.CharField("Tên đầy đủ",max_length=255)
#     address = models.TextField("Địa chỉ")
#     birth_date = models.DateField("Ngày sinh")
#     current_school = models.CharField("Trường đang dạy", max_length=255)
#     teacher_code = models.CharField("Mã giảng viên", max_length=10, unique=True, editable=False)

#     def save(self, *args, **kwargs):
#         if not self.teacher_code:
#             last_teacher = Teacher.objects.order_by('-id').first()
#             self.teacher_code = f"GV{(last_teacher.id + 1) if last_teacher else 1:04d}"
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return f"{self.full_name} - {self.teacher_code}"

# class Class(models.Model):
#     class_name = models.CharField("Tên lớp học", max_length=255, unique=True)
#     schedule = models.TextField("Lịch học") 
#     start_date = models.DateField("Ngày bắt đầu")
#     end_date = models.DateField("Ngày kết thúc")
#     teacher = models.OneToOneField(
#         Teacher, on_delete=models.SET_NULL, null=True, related_name="class_assigned"
#     )

#     def __str__(self):
#         return self.class_name

# class Enrollment(models.Model):
#     student = models.ForeignKey(
#         Student, on_delete=models.CASCADE, related_name="enrollments"
#     )
#     class_enrolled = models.ForeignKey(
#         Class, on_delete=models.CASCADE, related_name="enrolled_students"
#     )
#     status_choices = [
#         ('active', 'Đang học'),
#         ('transferred', 'Chuyển lớp'),
#         ('dropout', 'Nghỉ hẳn'),
#     ]
#     status = models.CharField(max_length=20, choices=status_choices, default='active')
#     enrollment_date = models.DateField(auto_now_add=True)
#     last_update = models.DateField(auto_now=True)

#     def __str__(self):
#         return f"{self.student} - {self.class_enrolled} ({self.get_status_display()})"

# class StudentHistory(models.Model):
#     student = models.ForeignKey(
#         Student, on_delete=models.CASCADE, related_name="history"
#     )
#     previous_class = models.ForeignKey(
#         Class, on_delete=models.SET_NULL, null=True, blank=True
#     )
#     action_choices = [
#         ('transferred', 'Chuyển lớp'),
#         ('dropout', 'Nghỉ hẳn'),
#     ]
#     action = models.CharField(max_length=20, choices=action_choices)
#     date = models.DateField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.student} - {self.get_action_display()} ({self.date})"

from django.contrib.auth.models import AbstractUser, User
from django.db import models
from django.utils.translation import gettext_lazy as _

# Chọn ngày trong tuần
class DayOfWeek(models.TextChoices):
    MONDAY = "Monday", _("Thứ Hai")
    TUESDAY = "Tuesday", _("Thứ Ba")
    WEDNESDAY = "Wednesday", _("Thứ Tư")
    THURSDAY = "Thursday", _("Thứ Năm")
    FRIDAY = "Friday", _("Thứ Sáu")
    SATURDAY = "Saturday", _("Thứ Bảy")
    SUNDAY = "Sunday", _("Chủ Nhật")

# Chọn buổi học
class SessionTime(models.TextChoices):
    MORNING = "Morning", _("Sáng")
    AFTERNOON = "Afternoon", _("Chiều")

# Học viên (Dùng bảng riêng)
class StudentUser(models.Model):
    full_name = models.CharField("Tên đầy đủ", max_length=255)
    address = models.TextField("Địa chỉ")
    birth_date = models.DateField("Ngày sinh")
    current_school = models.CharField("Trường đang theo học", max_length=255)
    parent_info = models.TextField("Thông tin phụ huynh")
    student_code = models.CharField("Mã học viên", max_length=10, unique=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.student_code:
            last_student = StudentUser.objects.order_by('-id').first()
            self.student_code = f"HS{(last_student.id + 1) if last_student else 1:04d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.full_name} - {self.student_code}"

# Lớp học (Liên kết với giáo viên từ bảng User)
class Class(models.Model):
    class_name = models.CharField("Tên lớp", max_length=255, unique=True)
    teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="classes")  # Liên kết với auth_user
    students = models.ManyToManyField(StudentUser, related_name="classes", blank=True)

    def __str__(self):
        return self.class_name

# Thời khóa biểu
class Schedule(models.Model):
    class_assigned = models.ForeignKey(Class, on_delete=models.CASCADE, related_name="schedules")
    teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="schedules")
    day_of_week = models.CharField(max_length=10, choices=DayOfWeek.choices)
    session = models.CharField(max_length=10, choices=SessionTime.choices)
    start_time = models.TimeField("Giờ bắt đầu")
    end_time = models.TimeField("Giờ kết thúc")
    room = models.CharField("Phòng học", max_length=50, blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["class_assigned", "day_of_week", "session"],
                name="unique_class_schedule"
            )
        ]

    def __str__(self):
        return f"{self.class_assigned} - {self.get_day_of_week_display()} ({self.get_session_display()})"
