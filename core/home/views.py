from django.shortcuts import render, redirect
from django.http import HttpResponse
from .utils import send_email_to_client, send_email_attachment
from django.conf import settings
from .models import *
import random


# Create your views here.
def home(request):
    context = {"page": "Home"}
    return HttpResponse("we are in Home")


def success_page(request):

    Car.objects.create(car_name=f"Nexon-{random.randint(0,100)}")
    people = [
        {"name": "Rishabh", "age": 27},
        {"name": "Deepanshu", "age": 25},
        {"name": "Sandeep", "age": 27},
        {"name": "Mukul", "age": 16},
        {"name": "Deep", "age": 14},
    ]
    return render(request, "index.html", context={"people": people, "page": "Contact"})


def send_email(request):
    subject = "This is a test mail"
    messege = "pohhooohhoo"
    sender = settings.EMAIL_HOST_USER
    file_path = f"{settings.BASE_DIR}/main.xlsx"
    recipient_list = ["hrishabhsoni412@gmail.com"]
    send_email_attachment(subject, messege, recipient_list, file_path)
    return redirect("/")
