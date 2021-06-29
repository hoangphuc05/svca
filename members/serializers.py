from django.contrib.auth.models import User, Group
from rest_framework import serializers

from . import models


class ReactMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ReactMember
        fields = ['id', 'name', 'contact_name', 'phone', 'email', 'contact_type', 'member_type', 'location_type','accepted']


class ReactNeedFullSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ReactNeed
        fields = ['id', 'first_name', 'last_name', 'phone', 'email', 'address', 'contact_reference', 'gender', 'ethnicity',
                  'relationship', 'language', 'vulnerable_groups', 'needs', 'date', 'state']


class ReactNeedSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ReactNeed
        fields = ['id', 'first_name', 'last_name', 'phone', 'email', 'contact_reference', 'gender',
                  'language', 'vulnerable_groups', 'needs', 'date']

class ReactNeedWorkingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ReactNeedWorking
        fields = ['id', 'date', 'agency', 'need', 'need_met', 'response']


class ReactFollowUpSerializer(serializers.ModelSerializer):
    class Meta:
        models = models.ReactFollowUp
        fields = ['id', 'worker', 'date', 'note', 'response']


class CustomTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CustomToken
        fields = ['devices', 'created']
