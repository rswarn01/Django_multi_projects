from django.db import models
from django.db.models.signals import post_save, pre_delete, pre_save, post_delete
from django.dispatch import receiver


# Create your models here.
class Student(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField(default=18)
    email = models.EmailField()
    address = models.TimeField()
    image = models.ImageField()
    file = models.FileField()


class Car(models.Model):
    car_name = models.CharField(max_length=100)
    speed = models.IntegerField(default=80)


# Signals
@receiver(post_save, sender=Car)
def call_car_singal(sender, instance, **kwargs):
    print("car created")
    print(sender, instance, kwargs)
