import random
from faker import Faker
from django.core.management.base import BaseCommand
from .models import Student, Teacher, Class, Enrollment, StudentHistory

fake = Faker("vi_VN")  # Tạo dữ liệu Tiếng Việt

class Command(BaseCommand):
    help = "Generate fake data for the database"

    def handle(self, *args, **kwargs):
        self.create_teachers(10)
        self.create_students(50)
        self.create_classes(5)
        self.create_enrollments(50)
        self.create_student_history(20)
        self.stdout.write(self.style.SUCCESS("Fake data generated successfully!"))

    def create_teachers(self, num):
        teachers = []
        for _ in range(num):
            teacher = Teacher(
                full_name=fake.name(),
                address=fake.address(),
                birth_date=fake.date_of_birth(minimum_age=25, maximum_age=60),
                current_school=fake.company()
            )
            teacher.save()
            teachers.append(teacher)
        return teachers

    def create_students(self, num):
        students = []
        for _ in range(num):
            student = Student(
                full_name=fake.name(),
                address=fake.address(),
                birth_date=fake.date_of_birth(minimum_age=6, maximum_age=18),
                current_school=fake.company(),
                parent_info=f"{fake.name()} - {fake.phone_number()}"
            )
            student.save()
            students.append(student)
        return students

    def create_classes(self, num):
        teachers = list(Teacher.objects.all())
        classes = []
        for i in range(num):
            class_obj = Class(
                class_name=f"Lớp {i+1} - {fake.word()}",
                schedule=random.choice(["Thứ 2 - Thứ 4", "Thứ 3 - Thứ 5", "Thứ 6 - Thứ 7"]),
                start_date=fake.date_between(start_date="-1y", end_date="today"),
                end_date=fake.date_between(start_date="today", end_date="+1y"),
                teacher=random.choice(teachers) if teachers else None
            )
            class_obj.save()
            classes.append(class_obj)
        return classes

    def create_enrollments(self, num):
        students = list(Student.objects.all())
        classes = list(Class.objects.all())
        statuses = ["active", "transferred", "dropout"]
        
        for _ in range(num):
            if students and classes:
                enrollment = Enrollment(
                    student=random.choice(students),
                    class_enrolled=random.choice(classes),
                    status=random.choice(statuses)
                )
                enrollment.save()

    def create_student_history(self, num):
        students = list(Student.objects.all())
        classes = list(Class.objects.all())
        actions = ["transferred", "dropout"]
        
        for _ in range(num):
            if students and classes:
                history = StudentHistory(
                    student=random.choice(students),
                    previous_class=random.choice(classes),
                    action=random.choice(actions),
                    date=fake.date_between(start_date="-6m", end_date="today")
                )
                history.save()
