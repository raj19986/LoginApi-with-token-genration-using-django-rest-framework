import random

from django.shortcuts import render
from rest_framework import permissions, generics, status
from django.contrib.auth import login
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User ,PhoneOTP
from .serializer import CreateUserSerializer
from django.shortcuts import get_object_or_404
from knox.auth import TokenAuthentication
from knox.views import LoginView as KnoxLoginView
from .serializer import LoginUserSerializer


class signup(APIView):
    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phone')
        if phone_number:
            phone = str(phone_number)
            user = User.objects.filter(phone__iexact=phone)
            if user.exists():
                return Response({
                    'status': False,
                    'detail': 'Phone Number already exists'
                })
            else:
                key=send_otp(phone)
                if key:
                    old=PhoneOTP.objects.filter(phone__iexact = phone)
                    if old.exists():
                        old=old.first()
                        count=old.count
                        if count >5:
                            return Response({
                                'status' : 1003,
                                'detail': 'sending otp eror limit exceded'
                            })
                        old.count=count+1
                        old.save()
                        print("count increase",count)
                        return Response({
                            'status' : '1003',
                            'detail' : 'Verification OTP Sent on the Mobile Number'
                        })
                    else:
                        PhoneOTP.objects.create(
                            phone=phone,
                            otp=key,
                        )
                        print("phone no is created for phone no=",phone,key)
                        old = PhoneOTP.objects.filter(phone__iexact=phone)
                        if old.exists():
                            print("pass ho gya maadi")
                        return Response({
                            'status' : '1003',
                            'detail' : 'Verification OTP Sent on the Mobile Number'
                        })

                else:
                    return Response({
                        'status': 1003,
                        'detail': 'OTP functionality issue'
                    })

        else:
            return Response({
                'status' : 1003,
                'detail' : 'phone error'
            })


def send_otp(phone):
    if phone:
        key=random.randint(1000,9000)
        print(key)
        return key

    else:
        return False


class VerifyOTP(KnoxLoginView):#APIView):KnoxLoginView
    #permission_classes = ()
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        phone = request.data.get('phone', False)
        otp_sent = request.data.get('otp', False)
        if phone and otp_sent:
            #print('phone aaya: ',phone)
            old = PhoneOTP.objects.filter(phone__iexact=phone)
            if old.exists():
                old = old.first()
                otp = old.otp
                if str(otp) == str(otp_sent):
                    old.validated = True
                    old.save()

                    #phone, password, customer_name = 'Bablu', dob = '1998-11-2', email = 'rajukaju@gmail.com', createdDate = '2021-12-2', is_staff = False, is_active = True, is_admin = False):

                    #Temp_data = {'phone': phone, 'password': '123456789','customer_name': 'Bablu', 'dob': '1998-11-2', 'email' : 'rajukaju@gmail.com', 'createdDate' : '2021-12-2' }
                    Temp_data = {'phone': phone, 'password': '123456789'}
                    serializer = CreateUserSerializer(data=Temp_data)
                    serializer.is_valid(raise_exception=True)
                    user = serializer.save()

                    #old.delete()

                    #permission_classes = (permissions.AllowAny,)
                    Temp_data = {'phone': phone, 'password': '123456789'}
                    serializer = LoginUserSerializer(data = Temp_data)#data=request.data)
                    serializer.is_valid(raise_exception=True)
                    user = serializer.validated_data['user']
                    login(request, user)

                    request =  super().post(request, format=None,)
                    #print(request.data['token'])
                    request.data['Status'] = 172917291729
                    token = request.data['token']
                    print(request.data)
                    return  Response({
                        'status': 1002,
                        'token': token
                    })
                    #return Response({"data": request.data})

                else:
                    return Response({
                        'status': 1002,
                        'detail': 'OTP incorrect '
                    })
            else:
                return Response({
                    'status': 1001,
                    'detail': 'Phone Error'
                })


        else:
            return Response({
                'status': '1001',
                'detail': 'Phone or OTP invalid'
            })

