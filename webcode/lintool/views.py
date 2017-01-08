from django.shortcuts import render
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponse

from loopwork import test_view
def test(request):
    user= User.objects.filter(username='coblan')
    user.encode('utf8')
    #send_mail('hello','i m heyulin','coblan@163.com',['he_yulin@163.com'])
    return render(request,'test.html')

def test_loopwork(request):
    dog = test_view()
    return HttpResponse(dog)