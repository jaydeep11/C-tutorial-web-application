from django import forms
from django.contrib.auth.models import User
from home.models import student

class registerUserForm(forms.Form):
    username=forms.CharField(max_length=50)
    password=forms.CharField(max_length=32,widget=forms.PasswordInput)
    passwordAgain=forms.CharField(max_length=32,widget=forms.PasswordInput)
    first_name=forms.CharField(max_length=30)
    last_name=forms.CharField(max_length=30)
    email=forms.EmailField(max_length=256)
    class Meta:
        model=User
        fields=('username','password','first_name','last_name','email')
    
class studentRegisterForm(registerUserForm):
    collage_name=forms.CharField(max_length=256)
    class Meta:
        model=student
        fields=('username','password','first_name','last_name','email','collage_name')