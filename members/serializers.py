from django.contrib.auth.models import User, Group
from rest_framework import serializers

from . import models


class ReactMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ReactMember
        fields = ['name', 'contact_name', 'phone', 'email', 'contact_type', 'member_type', 'location_type' ,'accepted']