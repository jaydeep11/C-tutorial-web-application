from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.views.decorators.cache import never_cache
from django.contrib.auth.hashers import make_password
from home.models import CPerson , student
from . import forms

from django.core.mail import send_mail
from django.conf import settings
# Create your views here.
def index(request):
    return HttpResponse('You\'re on accounts page' )

class signupUser(View):
    temp_name='accounts/signup.html'
    message=""
    def get(self,request):
        form=forms.studentRegisterForm()
        return render(request,self.temp_name,{'form':form})
    def post(self,request):
        form=forms.studentRegisterForm(request.POST)
        if form.is_valid() and form.cleaned_data['password']==form.cleaned_data['passwordAgain']:
            username=form.cleaned_data['username']
            err=False;
            try:
                user=User.objects.get(username=username)
                message="Username Exists!! Try another"
                form=forms.studentRegisterForm()
                return render(request,'accounts/signup.html',{'message':message,'form':form,})
            except:
                first_name=form.cleaned_data['first_name']
                last_name=form.cleaned_data['last_name']
                email=form.cleaned_data['email'] 
                collage_name=form.cleaned_data['collage_name']
                password=form.cleaned_data['password']
                password=make_password(password,salt=None,hasher='default')
                user=User(username=username,password=password,first_name=first_name,last_name=last_name,email=email)
                user.save()
                person=CPerson(user=user)
                person.save()
                stu=student(cperson=person,collage_name=collage_name)
                stu.save()
                wel_message='Hi'+first_name+last_name+'.'+'Welcome to JDPTUTS.Let us learn for a better future' 
                send_mail('Welcome',
                         wel_message,
                         settings.EMAIL_HOST_USER,
                         [email],
                         fail_silently=False)
                login(request,user)
                return redirect('tutorials:stu_home')
        else:
            message="Check whether password and confirm password field are same or not"
            form=forms.studentRegisterForm()
            return render(request,'accounts/signup.html',{'message':message,'form':form,})   
                
#@never_cache
class loginUser(View):
    temp_name='accounts/login.html'
    @never_cache
    def get(self,request):
        if request.user.is_authenticated==True:
            return redirect('tutorials:stu_home')
        else:
            return render(request,self.temp_name)
    @never_cache
    def post(self,request):
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(username=username,password=password)
        if user is not None:
            if user.is_active:
                login(request,user)
                return redirect('tutorials:stu_home')
        else:
            message="Please enter correct username and password"
            return render(request,self.temp_name,{'message':message,})
    
    
class logout_user(View):
    @never_cache
    def post(self,request):
        logout(request)
        return redirect('accounts:login')
    
    