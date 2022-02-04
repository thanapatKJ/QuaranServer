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

from django.contrib.auth import authenticate
from django.core.mail import send_mail
# from QuaranServer.settings import EMAIL_HOST_USER

class register(APIView):
    permission_classes = [AllowAny]
    
    def post(self,request):
        print("status IN")
        try:
            data = json.loads(request.body)
            user = User.objects.create_user(
                username=data['id_cards'],
                first_name=data['first_name'],
                last_name=data['last_name'],
                email=data['email'],
                password=data['password'],
                id_cards=data['id_cards'],
                numbers=data['numbers'],
            )
            token = Token.objects.create(user=user)
        except:
            pass
        else:
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
                'start_datetime':str(quarantine_data.start_date),
                'end_datetime':str(quarantine_data.start_date + timedelta(days=30)),
            }
        return Response(object)

    # DELETE ใช้ในการลบข้อมูลการเข้า quarantine
    def delete(self,request,format=None):
        user = User.objects.filter(username=request.user.username).first()
        quarantine_data = Quarantine.objects.filter(user=user).first().delete()
        object = {'status':'success'}
        return Response(object)

    # POST ใช้ในการรับค่าจาก Client ในหน้า QuarantinePlace ในการสร้างสถานที่ Quarantine
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
                    radius=data['radius'],
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
