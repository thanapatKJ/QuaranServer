
from django.http import HttpResponse
from datetime import datetime, timedelta

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