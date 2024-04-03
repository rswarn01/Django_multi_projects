from faker import Faker
import random
from .models import *
from accounts.models import *
from django.db.models import Sum

fake = Faker()


def create_marks(n):
    try:
        student_obj = Student.objects.all()
        for student in student_obj:
            subject = Subject.objects.all()
            for subject in subject:
                StudentMarks.objects.create(
                    subject=subject, student=student, marks=random.randint(0, 100)
                )
    except Exception as e:
        print(e)


def generate_report_card():
    ranks = Student.objects.annotate(marks=Sum("studentmarks__marks")).order_by(
        "-marks"
    )
    i = 1
    for rank in ranks:
        ReportCard.objects.create(student=rank, student_rank=i)
        i += 1


def seed_db(n=10) -> None:
    try:
        for i in range(n):
            department_obj = Department.objects.all()
            department_index = random.randint(0, len(department_obj) - 1)
            department = department_obj[department_index]

            student_id = f"STU-0{random.randint(100,999)}"
            student_name = fake.name()
            student_email = fake.email()
            student_age = random.randint(20, 30)
            student_address = fake.address()

            student_id_obj = StudentID.objects.create(student_id=student_id)

            student_obj = Student.objects.create(
                department=department,
                student_id=student_id_obj,
                student_name=student_name,
                student_email=student_email,
                student_age=student_age,
                student_address=student_address,
            )

    except Exception as ex:
        print(ex)
