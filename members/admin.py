from django.contrib import admin
from .models import ReactMember, CustomUser

# Register your models here.
admin.site.register(ReactMember)
admin.site.register(CustomUser)