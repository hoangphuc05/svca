from django.contrib.auth.models import User, Group
from rest_framework import serializers

from . import models


class ReactMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ReactMember
        fields = ['id', 'name', 'contact_name', 'phone', 'email', 'contact_type', 'member_type', 'location_type','accepted']


class ReactVulnerableGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ReactVulnerableGroup
        fields = ['name']

    def to_representation(self, value):
        return value.name

class ReactVulnerableIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ReactVulnerableGroup
        fields = ['name']


# class ReactNeedFullUpdateSerializer(serializers.ModelSerializer):
#     vulnerable_groups = ReactVulnerableIdSerializer(many=True)
#
#     class Meta:
#         model = models.ReactNeed
#         fields = ['id', 'first_name', 'last_name', 'phone', 'email', 'address', 'contact_reference', 'gender', 'ethnicity',
#                   'relationship', 'language', 'vulnerable_groups', 'needs', 'date', 'state', 'family18', 'family19', 'family55']


class ReactNeedFullSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ReactNeed
        fields = ['id', 'first_name', 'last_name', 'phone', 'email', 'address', 'contact_reference', 'gender', 'ethnicity',
                  'relationship', 'language', 'vulnerable_groups', 'needs', 'date', 'state', 'family18', 'family19', 'family55']


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
        model = models.ReactFollowUp
        fields = ['id', 'worker', 'date', 'note', 'response']


class ReactNeedAssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ReactNeedAssessment
        fields = ['id', 'assessment', 'date', 'author','response']


class CustomTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CustomToken
        fields = ['id', 'devices', 'created']


class UserProfileChangeSerializer(serializers.ModelSerializer):
    # username = models.CharField(required=False, allow_blank=True, initial="current username")
    class Meta:
        model = models.CustomUser
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email'
        ]

class ChangePasswordSerializers(serializers.Serializer):
    '''
    Serializer for changing password
    '''
    model = models.CustomUser
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    repeat_new_password = serializers.CharField(required=True)
