
from django.http import HttpResponse
from datetime import datetime, timedelta

from django.core.mail import send_mail
from QuaranServer.settings import EMAIL_HOST_USER

def check_time(request):
    object = datetime.now()
    # dt = datetime.strptime("21:00","%H:%M").time()
    # now = datetime.strptime("00:00","%H:%M").time()
    # result = ''
    # if now > dt:
    #     result = "Over 00:00"
    # else:
    #     result = "asdlo"
    result = (datetime.now()+timedelta(hours=3)).time()
    return HttpResponse(result)

def check_mail(request):
    message = "You are outside of your quarantine place."
    subject = 'Please go inside your quarantine place within 30 minutes.'
    send_mail(subject,message,EMAIL_HOST_USER,['thanapatkjm@gmail.com'],fail_silently=False)