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
