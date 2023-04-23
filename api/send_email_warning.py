from django.core.mail import send_mass_mail
from QuaranServer.settings import EMAIL_HOST_USER

from database.models import User, FaceData, Quarantine, History, QuarantineDay
from datetime import datetime, timedelta

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