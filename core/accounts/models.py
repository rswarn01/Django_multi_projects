from django.db import models
from veggie.models import *
from django.contrib.auth.models import AbstractUser

# Create your models here.


class Subject(models.Model):
    subject_name = models.CharField(max_length=100)

    def __str__(self):
        return self.subject_name


class StudentMarks(models.Model):
    student = models.ForeignKey(
        Student, related_name="studentmarks", on_delete=models.CASCADE
    )
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    marks = models.IntegerField()

    def __str__(self):
        return f"{self.student.student_name} {self.subject.subject_name} {self.marks}"

    class Meta:
        unique_together = ["student", "subject"]


class ReportCard(models.Model):
    student = models.ForeignKey(
        Student, related_name="studentreportcard", on_delete=models.CASCADE
    )
    student_rank = models.IntegerField()
    date = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ["student_rank", "date"]


# class CustomUser(AbstractUser):
#     username = None
#     phone_number = models.CharField(max_length=100, unique=True)
#     email = models.EmailField(unique=True)
#     user_bio = models.CharField(max_length=100)
#     user_dp = models.ImageField(upload_to="profile")

#     USERNAME_FIELD = "phone_number"
#     REQUIRED_FIELDS = []
