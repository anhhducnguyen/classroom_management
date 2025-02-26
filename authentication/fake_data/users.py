from faker import Faker
import json
from datetime import datetime
import pytz  

fake = Faker()
users = []

timezone = pytz.timezone("Asia/Ho_Chi_Minh")  # Thay bằng múi giờ của bạn
password = "pbkdf2_sha256$720000$wjIUeFinTjPebKdlXc4jYG$7WYDyYXPM3/6hKyMiR2QXeVRd6CHGSapTxYW2C+rUAM=";

for i in range(50):  # Tạo 50 người dùng mẫu
    date_joined_naive = fake.date_time_this_year()  # Tạo naive datetime
    date_joined_aware = timezone.localize(date_joined_naive)  # Chuyển thành aware datetime

    users.append({
        "model": "auth.user",
        "pk": i + 1,
        "fields": {
            "username": fake.user_name(),
            "password": password,
            "is_superuser": False,
            "is_staff": False,
            "is_active": True,
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "email": fake.email(),
            "date_joined": date_joined_aware.isoformat(),  # Ghi aware datetime
        }
    })

with open("authentication/fixtures/user.json", "w") as f:
    json.dump(users, f, indent=4)

print(f"Created {len(users)} users")