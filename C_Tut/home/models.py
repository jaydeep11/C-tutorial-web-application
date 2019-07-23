from django.db import models
from django.contrib.auth.models import User


class CPerson(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    types=(
        ('student','student'),
    )
    type=models.CharField(max_length=20,choices=types,default='student')
    
    def __str__(self):
        return self.user.first_name+" "+self.user.last_name
    
class student(models.Model):
    cperson=models.OneToOneField(CPerson,on_delete=models.CASCADE)
    collage_name=models.CharField(max_length=100)
    progress=models.IntegerField(default=1)
    
    def __str__(self):
        return self.cperson.user.first_name+" "+self.cperson.user.last_name