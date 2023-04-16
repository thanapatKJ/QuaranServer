from django.core.mail import send_mass_mail
from QuaranServer.settings import EMAIL_HOST_USER

from database.models import User, FaceData, Quarantine, History, QuarantineDay
from datetime import datetime, timedelta

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
    print('send_email_inactive')
    message = "Your quarantine status is inactivated.\nPlease contact the QuaranClean's administrator to activate your status."+"\nTime: "+str(datetime.now().hour)+":"+str(datetime.now().minute)
    user_list = Quarantine.objects.filter(quarantine_status='unverified')
    subject = 'Your quarantine status is inactivated.'
    recipient = []
    for user in user_list:
        recipient.append(user.user.email)
    user_list.update(quarantine_status='inactive')
    messages = [(subject,message,EMAIL_HOST_USER,[re]) for re in recipient]
    send_mass_mail(messages)
    print('inactive : '+str(datetime.now()))

def end_quarantine():
    quarantine_data = Quarantine.objects.exclude(quarantine_status='inactive')
    recipient = []
    quarantine_day= QuarantineDay.objects.all().first().days
    # print(datetime.now())
    for each in quarantine_data:
        start = each.start_date.strftime('%d-%m-%Y')
        end = datetime.strptime(start, '%d-%m-%Y') + timedelta(days=quarantine_day)
        start = datetime.strptime(start, '%d-%m-%Y')
        # print(start - timedelta(days=15))
        if datetime.now() >= end :
            print('end of Quarantine for '+each.user.first_name)
            recipient.append(each.user.email)
    message = "Congratulation, it's the end of your quarantine. \nGod bless you."
    subject = 'End of your quarantine.'
    messages = [(subject,message,EMAIL_HOST_USER,[re]) for re in recipient]
    send_mass_mail(messages)
    for user in recipient: 
        Quarantine.objects.get(user__email=user).delete()
    print('end_quarantine : '+str(datetime.now()))
