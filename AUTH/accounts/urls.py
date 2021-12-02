from django.urls import path, include, re_path
from knox import views as knox_views
from .views import *
app_name='accounts'

urlpatterns = [

    re_path(r'^signup/' , signup.as_view()),
    re_path("^verify_otp/$" , VerifyOTP.as_view()),
]




