
from django.http import HttpResponse
from datetime import datetime

def check_time():
    object = datetime.now()
    return HttpResponse(object)