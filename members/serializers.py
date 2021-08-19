from django.contrib.auth.models import User, Group
from rest_framework import serializers
from rest_framework.exceptions import ErrorDetail, ValidationError
from django.core.exceptions import ValidationError as DjangoValidationError


from . import models


class ReactMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ReactMember
        fields = ['id', 'name', 'contact_name', 'phone', 'email', 'contact_type', 'member_type', 'location_type','accepted']


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['name']

    def to_representation(self, value):
        return value.name


class UserSerializer(serializers.ModelSerializer):
    # groups = GroupSerializer(many=True)

    class Meta:
        model = models.CustomUser
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'date_joined', 'groups']
        read_only_fields = ['id', 'date_joined']


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
                  'relationship', 'language', 'vulnerable_groups', 'needs', 'date', 'housing', 'state', 'family18', 'family19', 'family55',
                  'state']

    def run_validation(self, data):
        if 'vulnerable_groups' not in data:
            pass
        elif type(data['vulnerable_groups']) == list:
            # If a list of vulnerabe group present, create any new group in this request - made for future proof
            for group in data['vulnerable_groups']:
                vuln_obj, created = models.ReactVulnerableGroup.objects.get_or_create(name=group)
        else:
            raise serializers.ValidationError("vulnerable_groups is not a list")

        (is_empty_value, data) = self.validate_empty_values(data)
        if is_empty_value:
            return data

        value = self.to_internal_value(data)
        try:
            self.run_validators(value)
            value = self.validate(value)
            assert value is not None, '.validate() should return the validated data'
        except (ValidationError, DjangoValidationError) as exc:
            raise ValidationError(detail="error")

        return value

    # def validate_vulnerable_groups(self, value):
    #     if type(value) == list:
    #         for group in value:
    #             vuln_obj, created = models.ReactVulnerableGroup.objects.get_or_create(name=group)
    #     else:
    #         raise serializers.ValidationError("vulnerable_groups is not a list")
    #     return value


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


class UserSignupSerializers(serializers.Serializer):
    """
    Serializers for creating new user
    """

    models = models.CustomUser
    username = serializers.CharField(required=True)
    email = serializers.CharField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)


class UserGroupUpdateSerializers(serializers.Serializer):
    """
    Serializers for updating user's group
    """
    model = models.CustomUser
    username = serializers.CharField(required=True)
    groups = serializers.ListField(child=serializers.CharField())


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['name']

    def to_representation(self, value):
        return value.name

class UserInfo(serializers.ModelSerializer):
    groups = GroupSerializer(many=True)
    class Meta:
        model = models.CustomUser
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'groups']