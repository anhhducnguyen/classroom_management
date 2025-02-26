import os
import json
from faker import Faker
from datetime import datetime, timedelta
import random

# Khởi tạo Faker
fake = Faker("vi_VN")

# Đảm bảo thư mục fixtures tồn tại
os.makedirs("fixtures", exist_ok=True)

# Số lượng dữ liệu mỗi bảng
NUM_RECORDS = 50

# Danh sách chứa dữ liệu JSON
students = []
teachers = []
classes = []
enrollments = []
student_histories = []

# 📌 1. Fake dữ liệu cho bảng `Teacher`
for i in range(1, NUM_RECORDS + 1):
    birth_date = fake.date_of_birth(minimum_age=25, maximum_age=60).strftime("%Y-%m-%d")
    teachers.append({
        "model": "authentication.Teacher",
        "pk": i,
        "fields": {
            "full_name": fake.name(),
            "address": fake.address(),
            "birth_date": birth_date,
            "current_school": fake.company(),
            "teacher_code": f"GV{i:04d}"
        }
    })

# 📌 2. Fake dữ liệu cho bảng `Class`
for i in range(1, NUM_RECORDS + 1):
    start_date = fake.date_between(start_date="-2y", end_date="today").strftime("%Y-%m-%d")
    end_date = (datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=365)).strftime("%Y-%m-%d")
    classes.append({
        "model": "authentication.Class",
        "pk": i,
        "fields": {
            "class_name": f"Lớp {random.randint(1, 12)}-{fake.random_element(['A', 'B', 'C', 'D'])}",
            "schedule": fake.random_element(["Thứ 2, Thứ 4, Thứ 6", "Thứ 3, Thứ 5, Thứ 7"]),
            "start_date": start_date,
            "end_date": end_date,
            "teacher": i if i <= len(teachers) else None
        }
    })

# 📌 3. Fake dữ liệu cho bảng `Student`
for i in range(1, NUM_RECORDS + 1):
    birth_date = fake.date_of_birth(minimum_age=6, maximum_age=18).strftime("%Y-%m-%d")
    students.append({
        "model": "authentication.Student",
        "pk": i,
        "fields": {
            "full_name": fake.name(),
            "address": fake.address(),
            "birth_date": birth_date,
            "current_school": fake.company(),
            "parent_info": fake.name() + " - " + fake.phone_number(),
            "student_code": f"HS{i:04d}"
        }
    })

# 📌 4. Fake dữ liệu cho bảng `Enrollment`
for i in range(1, NUM_RECORDS + 1):
    enrollments.append({
        "model": "authentication.Enrollment",
        "pk": i,
        "fields": {
            "student": random.randint(1, NUM_RECORDS),
            "class_enrolled": random.randint(1, NUM_RECORDS),
            "status": fake.random_element(["active", "transferred", "dropout"]),
            "enrollment_date": fake.date_between(start_date="-2y", end_date="today").strftime("%Y-%m-%d"),
            "last_update": fake.date_between(start_date="-1y", end_date="today").strftime("%Y-%m-%d")
        }
    })

# 📌 5. Fake dữ liệu cho bảng `StudentHistory`
for i in range(1, NUM_RECORDS + 1):
    student_histories.append({
        "model": "authentication.StudentHistory",
        "pk": i,
        "fields": {
            "student": random.randint(1, NUM_RECORDS),
            "previous_class": random.randint(1, NUM_RECORDS),
            "action": fake.random_element(["transferred", "dropout"]),
            "date": fake.date_between(start_date="-2y", end_date="today").strftime("%Y-%m-%d")
        }
    })

# 📌 Lưu các file JSON vào thư mục `fixtures/`
fixtures = {
    "students.json": students,
    "teachers.json": teachers,
    "classes.json": classes,
    "enrollments.json": enrollments,
    "student_histories.json": student_histories
}

for filename, data in fixtures.items():
    with open(f"authentication/fixtures/{filename}", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

print(f"✅ Đã tạo dữ liệu giả và lưu vào thư mục 'fixtures/'")
