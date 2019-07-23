from django import forms
from .models import Contact

class contactForm(forms.Form):
    first_name=forms.CharField(max_length=30)
    last_name=forms.CharField(max_length=30)
    email=forms.EmailField(max_length=256)
    message=forms.CharField(widget=forms.Textarea)
    
    class Meta:
        model=Contact
        fields=('first_name','last_name','email','message')