from django.contrib import admin
from .models import Contact
# Register your models here.
class ContactAdmin(admin.ModelAdmin):
    readonly_fields = ["first_name","last_name","email","message"]
admin.site.register(Contact,ContactAdmin)