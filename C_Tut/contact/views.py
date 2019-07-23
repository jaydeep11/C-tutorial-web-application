from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from . import forms
from .models import Contact
# Create your views here.
def contact(request):
    temp_name='home/contact.html'
    
    if request.method=="GET":
        form=forms.contactForm()
        context={
            'form':form,
        }
        return render(request,temp_name,context)

    else:
        form=forms.contactForm(request.POST)
        
        if form.is_valid():
            first_name=form.cleaned_data['first_name']
            last_name=form.cleaned_data['last_name']
            email=form.cleaned_data['email'] 
            message=form.cleaned_data['message']
            contact=Contact(first_name=first_name,last_name=last_name,email=email,message=message)
            contact.save()
            form=forms.contactForm()
            message="We will respond Soon...........Thankyou!!!"
            context={
                'message':message,
                'form':form,
            }
            return render(request,temp_name,context)
        
    