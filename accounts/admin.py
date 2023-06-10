from django.contrib import admin
from .models import CustomUser, Interest 

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Interest)