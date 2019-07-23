from django.db import models

# Create your models here.
class Tutorial(models.Model):
    name=models.CharField(max_length=300)
    html_name=models.CharField(max_length=300)
    created_date=models.DateTimeField('date published')
    
    def __str__(self):
        return self.name