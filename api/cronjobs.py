from datetime import datetime
from django.core.mail import send_mass_mail
from QuaranServer.settings import EMAIL_HOST_USER

from database.models import User, FaceData, Quarantine, History

def send_email_check():
    message = "Please Verify yourself via QuaranClean application inside your quarantine place within 30 minutes"+"\nTime: "+str(datetime.now().hour)+":"+str(datetime.now().minute)
    quarantine_set = Quarantine.objects.exclude(quarantine_status='inactive')
    quarantine_set.update(quarantine_status='unverified')
    subject = 'Please verify yourself.'
    user_list = Quarantine.objects.exclude(quarantine_status='inactive')
    print(user_list)
    recipient = []
    for user in user_list:
        recipient.append(user.user.email)
    print(recipient)
    messages = [(subject,message,EMAIL_HOST_USER,[re]) for re in recipient]
    send_mass_mail(messages)

def send_email_warning():
    subject = 'Please verify yourself (warning).'
    message = "Please Verify yourself via QuaranClean application inside your quarantine place within 15 minutes"+"\nTime: "+str(datetime.now().hour)+":"+str(datetime.now().minute)
    user_list = Quarantine.objects.filter(quarantine_status='unverified')
    print(user_list)
    recipient = []
    for user in user_list:
        recipient.append(user.user.email)
    print(recipient)
    messages = [(subject,message,EMAIL_HOST_USER,[re]) for re in recipient]
    send_mass_mail(messages)
    print('warning : '+str(datetime.now()))
    
def send_email_inactive():
    message = "Your quarantine status is inactivated.\nPlease contact the QuaranClean's administrator to activate your status."+"\nTime: "+str(datetime.now().hour)+":"+str(datetime.now().minute)
    user_list = Quarantine.objects.filter(quarantine_status='unverified')
    user_list.update(quarantine_status='inactive')
    subject = 'Your quarantine status is inactivated.'
    print(user_list)
    recipient = []
    for user in user_list:
        recipient.append(user.user.email)
    print(recipient)
    messages = [(subject,message,EMAIL_HOST_USER,[re]) for re in recipient]
    send_mass_mail(messages)
    print('inactive : '+str(datetime.now()))

def end_quarantine():
    message = "Please Verify yourself via QuaranClean application inside your quarantine place within 30 minutes"+"\nTime: "+str(datetime.now().hour)+":"+str(datetime.now().minute)
    quarantine_set = Quarantine.objects.exclude(quarantine_status='inactive')
    # quarantine_set.update(quarantine_status='unverified')
    subject = 'Please verify yourself.'
    user_list = Quarantine.objects.exclude(quarantine_status='inactive')
    print(user_list)
    recipient = []
    for user in user_list:
        recipient.append(user.user.email)
    print(recipient)
    messages = [(subject,message,EMAIL_HOST_USER,[re]) for re in recipient]
    send_mass_mail(messages)