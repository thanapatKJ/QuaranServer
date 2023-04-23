from django.core.mail import send_mass_mail
from QuaranServer.settings import EMAIL_HOST_USER

from database.models import User, FaceData, Quarantine, History, QuarantineDay
from datetime import datetime, timedelta

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