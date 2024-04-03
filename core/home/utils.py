from home.models import Student
import time
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.conf import settings


def send_email_to_client():
    subject = "This is a test mail"
    messege = "pohhooohhoo"
    sender = settings.EMAIL_HOST_USER
    recipient_list = [""]
    EmailMessage(subject, messege, recipient_list)


def send_email_attachment(subject, messege, recipient_list, file_path):
    mail = EmailMessage(
        subject=subject,
        body=messege,
        from_email=settings.EMAIL_HOST_USER,
        to=recipient_list,
    )
    mail.attach_file(file_path)
    mail.send()
