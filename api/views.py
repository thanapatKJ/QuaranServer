# from api.forms import UserForm
from database.models import History, User, FaceData, Quarantine
from django.http import HttpResponse, JsonResponse
from datetime import datetime, timedelta

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny,IsAuthenticated

import json
import threading
import time

from django.contrib.auth import authenticate
from django.core.mail import send_mail
from QuaranServer.settings import EMAIL_HOST_USER

class register(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        print("status IN")
        print(request.POST['id_cards'])
        user = User.objects.create_user(
            username=request.POST['id_cards'],
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            email=request.POST['email'],
            password=request.POST['password'],
            id_cards=request.POST['id_cards'],
            numbers=request.POST['numbers'],
            )
        Token.objects.create(user=user)
        # print(request.FILES['images'])
        FaceData.objects.create(
            user=user,
            image=request.FILES['image']
        )
        response = {'status':'success'}
        return Response(response)

class logout(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,format=None):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)

class Check(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,format=None):
        print("check In")
        user = User.objects.filter(username=request.user.username).first()
        object = {
            'status':'success',
            'username':user.username,
        }
        return Response(object)

class Profile(APIView):
    permission_classes = [IsAuthenticated]

    # Profile screen data
    def get(self,request,format=None):
        user = User.objects.filter(username=request.user.username).first()
        object = {
            'first_name':user.first_name,
            'last_name':user.last_name,
            'id_cards':user.id_cards,
            'numbers':user.numbers,
            'email':user.email
        }
        return Response(object)

    # Change Password
    def post(self,request,format=None):
        try:
            print('Password Change')
            data = json.loads(request.body)
            user = User.objects.filter(username=request.user.username).first()
            print(data['opassword'])
            check = authenticate(username=user.username,password=data['opassword'])
            if check is not None:
                user.set_password(data['npassword'])
                user.save()
                print('newPassword is '+data['npassword'])
            else:
                raise Exception('Old password is not correct')
        except:
            pass
        else:
            object = {
                'method':'ChangePassword',
                'status':'success'
                }
            return Response(object)


def exit(quarantine_data,second):
    print('exit '+str(quarantine_data.is_inside))
    quarantine_data.is_inside = False
    quarantine_data.save()
    quarantine_data.save()
    message = "You are outside of your quarantine place. " +str(datetime.now().hour)+":"+str(datetime.now().minute)
    subject = 'Please go inside your quarantine place within 30 minutes.'
    send_mail(subject,message,EMAIL_HOST_USER,[quarantine_data.user.email],fail_silently=False)
    time.sleep(second)
    if(not(quarantine_data.is_inside)):
        
        quarantine_data.quarantine_status = 'inactive'
        quarantine_data.save()
        message = "Your quarantine status is inactivated.\nPlease contact the QuaranClean's administrator to activate your status."+"\nTime: "+str(datetime.now().hour)+":"+str(datetime.now().minute)
        subject = 'Your quarantine status is inactivated.'
        send_mail(subject,message,EMAIL_HOST_USER,[quarantine_data.user.email],fail_silently=False)
        print('inactive')
    print('Exit already passed '+str(second))

def enter(quarantine_data,second):
    quarantine_data.is_inside = True
    quarantine_data.save()
    print('Enter already passed '+str(second))

class EnterExit(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request,format=None):
        data = json.loads(request.body)
        user = User.objects.filter(username=request.user.username).first()
        quarantine_data = Quarantine.objects.filter(user=user).first()
        action=''
        print(data['action'])
        if(data['action']=="enter"):
            thr = threading.Thread(target=enter, args=[quarantine_data, 10])
            action='enter'
        elif(data['action']=="exit"):
            thr = threading.Thread(target=exit, args=[quarantine_data, 1800])
            # thr = threading.Thread(target=exit, args=[quarantine_data, 10])

            action='exit'

        thr.start()
        print('return')
        object={
            'status':'success',
            'action': action
        }
        return Response(object)


class Quarantine_class(APIView):
    permission_classes = [IsAuthenticated]
    
    # GET ใช้ในการยืนยันในหน้า Home และหน้า QuarantinePlace เพื่อยืนยันว่ามีการ Quarantine อยู่หรือไม่
    def get(self,request,format=None):
        print('quarantine get')
        # try:
        user = User.objects.filter(username=request.user.username).first()
        quarantine_data = Quarantine.objects.filter(user=user).first()
        # print('try')
        print(quarantine_data)
        if quarantine_data is None:
            object = {
                'status':False,
                }
        else:
            print('None')
            object = {
                'status':True,
                'name':quarantine_data.name,
                'lat':quarantine_data.lat,
                'long':quarantine_data.long,
                'radius':quarantine_data.radius,
                'address':quarantine_data.address,
                'start_datetime':str((quarantine_data.start_date).strftime("%d/%m/%Y %H:%M")),
                'end_datetime':str((quarantine_data.start_date + timedelta(days=14)).strftime("%d/%m/%Y %H:%M")),
                'inside':quarantine_data.is_inside
            }
        return Response(object)

    # DELETE ใช้ในการลบข้อมูลการเข้า quarantine
    def delete(self,request,format=None):
        user = User.objects.filter(username=request.user.username).first()
        quarantine_data = Quarantine.objects.filter(user=user).first().delete()
        object = {'status':'success'}
        return Response(object)

    # POST ใช้ในการรับค่าจาก Client ในหน้า QuarantinePlace ในการสร้างสถานที่ Quarantine radius + 15
    def post(self,request,format=None):
        print('post quarantine')
        try:
            data = json.loads(request.body)
            user = User.objects.filter(username=request.user.username).first()
            quarantine_data = Quarantine.objects.filter(user=user).first()
            if quarantine_data is None:
                Quarantine.objects.create(
                    user=user,
                    name=data['name'],
                    lat=data['lat'],
                    long=data['long'],
                    radius=int(data['radius'])+15,
                    address=data['address'],
                    start_date=datetime.now())
            else:
                raise Exception('Already has quarantine data')
            print('try')
        except:
            print('except')
        else:
            print('else')
            object = {
                'method':'quarantine',
                'status':'success'
                }
            return Response(object)

class Verify(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,format=None):
        print('Verify get')
        user = User.objects.filter(username=request.user.username).first()
        quarantine_data = Quarantine.objects.filter(user=user).first()
        next = ''
        if quarantine_data is not None:
            print('not none')
            print(quarantine_data.quarantine_status)
            if quarantine_data.quarantine_status == 'verified':
                print('ver')
                now = datetime.now()
                status='verified'
                if (now+timedelta(hours=3)).time() >= datetime.strptime("21:00","%H:%M").time():
                    next = '21:00'
                    print('return next time = 21:00')
                elif (now+timedelta(hours=3)).time() >= datetime.strptime("18:00","%H:%M").time():
                    next = '18:00'
                    print('return next time = 18:00')
                elif (now+timedelta(hours=3)).time() >= datetime.strptime("15:00","%H:%M").time():
                    next = '15:00'
                    print('return next time = 15:00')
                elif (now+timedelta(hours=3)).time() >= datetime.strptime("12:00","%H:%M").time():
                    next = '12:00'
                    print('return next time = 12:00')
                else:
                    next = '9:00'
                    print('return next time = 9:00')
            elif quarantine_data.quarantine_status == 'unverified':
                print('unverified')
                status='unverified'
            elif quarantine_data.quarantine_status == 'inactive':
                print('inactive')
                status='inactive'
        else:
            status='None'
        object = {
            'status':status,
            'next_time':next}
        return Response(object)

    def post(self,request,format=None):
        print('Verify POST')
        user = User.objects.filter(username=request.user.username).first()
        data = json.loads(request.body)
        quarantine_data = Quarantine.objects.filter(user=user).first()
        History.objects.create(
            quarantine=quarantine_data,
            check_datetime=datetime.now(),
            lat_check=data['lat'],
            long_check=data['long']
            )
        quarantine_data.quarantine_status = "verified"
        quarantine_data.save()
        object = {'status':'success'}
        return Response(object)
