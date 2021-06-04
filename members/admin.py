from django.contrib import admin
from .models import ReactMember, ReactUser

# Register your models here.
admin.site.register(ReactMember)
admin.site.register(ReactUser)