# from api.forms import UserForm
from database.models import User, FaceData, Quarantine
from django.http import HttpResponse, JsonResponse
from datetime import datetime

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

class Quarantine(APIView):
    permission_classes = [IsAuthenticated]

    # GET ใช้ในการยืนยันในหน้า Home และหน้า QuarantinePlace เพื่อยืนยันว่ามีการ Quarantine อยู่หรือไม่
    def get(self,request,format=None):
        
        # object = {
        #     'status':'quarantine',
        #     'lat':'lat',
        #     'long':'long',
        #     'radius':'radius',
        #     'name':'placeName',
        #     'detail':'detail'
        #     }
        object = {
            'status':'none',
        }
        return Response(object)


    # POST ใช้ในการรับค่าจาก Client ในหน้า QuarantinePlace ในการสร้างสถานที่ Quarantine
    def post(self,request,format=None):
        try:
            data = json.loads(request.body)
            user = User.objects.filter(username=request.user.username).first()
            
        except:
            pass
        else:
            object = {
                'method':'quarantine',
                'status':'success'
                }
            return Response(object)
