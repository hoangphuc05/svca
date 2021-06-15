from django.contrib.auth.models import User, Group
from rest_framework import serializers

from . import models


class ReactMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ReactMember
        fields = ['id', 'name', 'contact_name', 'phone', 'email', 'contact_type', 'member_type', 'location_type','accepted']


class ReactNeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ReactNeed
        fields = ['id', 'name', 'time', 'state', 'email', 'phone', 'description']


class CustomTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CustomToken
        fields = ['devices', 'created']
