from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.utils.text import slugify

# User = get_user_model()
# Create your models here.


# Django manager is a class that acts as an interface through which Django models interact with databases.
# By default we have Objects model manager.
# to use a functinality without changing in Model/ change in queryset.
# we can create custom manager like below.
class StudentManager(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset().filter(is_deleted=False)


class Receipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    receipe_name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, default="")
    receipe_description = models.TextField()
    receipe_image = models.ImageField(upload_to="receipe")
    receipe_view_count = models.IntegerField(default=1)
    is_deleted = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.receipe_name)
        super(Receipe, self).save(*args, **kwargs)


# Create your models here.
class Department(models.Model):
    department = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.department

    class Meta:
        ordering = ["department"]


class StudentID(models.Model):
    student_id = models.CharField(max_length=100)

    def __str__(self):
        return self.student_id


class Student(models.Model):
    department = models.ForeignKey(
        Department, related_name="depart", on_delete=models.CASCADE
    )
    student_id = models.OneToOneField(
        StudentID, related_name="studentid", on_delete=models.CASCADE
    )
    student_name = models.CharField(max_length=100)
    student_email = models.EmailField(unique=True)
    student_age = models.IntegerField(default=18)
    student_address = models.TextField()
    is_deleted = models.BooleanField(default=False)

    objects = StudentManager()
    admin_objects = models.Manager()

    def __str__(self):
        return self.student_name

    class Meta:
        ordering = ["student_name"]
        verbose_name = "student"
