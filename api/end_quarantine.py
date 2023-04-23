from django.core.mail import send_mass_mail
from QuaranServer.settings import EMAIL_HOST_USER

from database.models import User, FaceData, Quarantine, History, QuarantineDay
from datetime import datetime, timedelta

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