from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from .models import Log, CustomUser
from log_project.celery import app 
import time

@shared_task()
def send_mail_to_user(self):
    print(">>>>>>>>>>>>>>>>>>>>>> send_mail_to_user >>>>>>>>>>>>>>>>>>>>>>>>>>")
    # time.sleep(60)
    logdata = list(Log.objects.filter(created_by__email = 'pratik@gmail.com').values())
    # recipient_list = list(CustomUser.objects.all().values_list('email', flat=True))
    recipient_list = ['pratik@yopmail.com']
    subject = 'Welcome To Log Project'
    message = f'Hello,\n I am pratik and This is my log details.'
    email_from = settings.EMAIL_HOST_USER
    send_mail(
        subject,
        message,
        email_from,
        recipient_list,
        html_message = render_to_string('info.html', {'log':logdata})
        )