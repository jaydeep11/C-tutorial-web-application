from django.contrib import admin
from .models import Tutorial
# Register your models here.
class TutorialAdmin(admin.ModelAdmin):
    list_filter=('created_date',)
admin.site.register(Tutorial,TutorialAdmin)