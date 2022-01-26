from django.contrib import admin

from .models import User, FaceData, Quarantine
# Register your models here.

admin.site.register(User)
admin.site.register(FaceData)
admin.site.register(Quarantine)