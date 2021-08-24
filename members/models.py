# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
import binascii
import os

from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from datetime import date


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    pass


class ReactMember(models.Model):
    name = models.CharField(max_length=255)
    contact_name = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, null=True)
    email = models.CharField(max_length=255)
    contact_type = models.IntegerField(default=0)
    member_type = models.IntegerField(default=0)
    location_type = models.IntegerField(default=0)
    accepted = models.IntegerField(blank=True, null=True)
    account = models.OneToOneField(CustomUser, on_delete=models.SET_NULL, null=True)

    class Meta:
        managed = True
        db_table = 'react_member'
        permissions = [
            ("is_member", "Is a member and can only view specific information")
        ]


class ReactVulnerableGroup(models.Model):
    class Meta:
        db_table = "react_vulnerable_group_name"
    name = models.CharField(max_length=255 ,primary_key=True)


class ReactNeed(models.Model):
    class Meta:
        db_table = 'react_need'
        # permissions = [
        #     ("need_admin", "full permission over needs model"),
        #     ("need_limited", "only view a limited information of a need")
        # ]
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    contact_reference = models.IntegerField(default=1)
    gender = models.CharField(max_length=255, blank=True, null=True)
    ethnicity = models.CharField(max_length=255, blank=True, null=True)
    relationship = models.CharField(max_length=255, blank=True, null=True)
    language = models.CharField(max_length=255, blank=True, null=True)
    # vulnerable_groups = models.ManyToManyField(ReactVulnerableGroup)
    vulnerable_groups = models.ManyToManyField(ReactVulnerableGroup)
    family18 = models.IntegerField(default=0)
    family19 = models.IntegerField(default=0)
    family55 = models.IntegerField(default=0)
    housing = models.IntegerField(default=-1)
    needs = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    state = models.IntegerField(null=False, default=0)

    def __str__(self):
        return '{self.first_name}'.format(self=self)


# this thing is not used anywhere?
class ReactNeedResponse(models.Model):
    class Meta:
        db_table = "react_need_response"

    client = models.ForeignKey(ReactNeed, on_delete=models.SET_NULL, null=True)
    need = models.TextField()
    date = models.DateTimeField()


class ReactNeedAssessment(models.Model):
    class Meta:
        db_table = "react_need_assessment"
    response = models.ForeignKey(ReactNeed, on_delete=models.SET_NULL, null=True, unique=True)
    assessment = models.TextField()
    date = models.DateField(null=True, default=date.today)
    author = models.TextField(max_length=255, null=True)


class ReactNeedWorking(models.Model):
    class Meta:
        db_table = "react_need_working"

    agency = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateField(null=True, auto_now_add=True)
    need = models.TextField(null=True)
    need_met = models.TextField(null=True)
    response = models.ForeignKey(ReactNeed, on_delete=models.SET_NULL, null=True)


class ReactFollowUp(models.Model):
    class Meta:
        db_table = "react_need_followup"

    worker = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateField(null=True, default=date.today)
    note = models.TextField()
    response = models.ForeignKey(ReactNeed, on_delete=models.SET_NULL, null=True)


# this model is not used anywhere
class ReactUser(models.Model):
    username = models.CharField(unique=True, max_length=255)
    avatar_url = models.CharField(max_length=200, blank=True, null=True)
    display_name = models.CharField(max_length=255, blank=True, null=True)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255)
    email = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=255, blank=True, null=True)
    user_type = models.IntegerField()

    class Meta:
        db_table = 'react_user'


class User(models.Model):
    username = models.CharField(max_length=255)
    avatar_url = models.CharField(max_length=2000, blank=True, null=True)
    display_name = models.CharField(max_length=255)
    full_name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    permission = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'user'


class CustomToken(models.Model):
    """
       Custom token model
    """
    key = models.CharField("Key", max_length=40, unique=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='custom_auth_token',
        on_delete=models.CASCADE, verbose_name="User"
    )
    created = models.DateTimeField("Created", auto_now_add=True)
    devices = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        # Work around for a bug in Django:
        # https://code.djangoproject.com/ticket/19422
        #
        # Also see corresponding ticket:
        # https://github.com/encode/django-rest-framework/issues/705
        # abstract = 'rest_framework.authtoken' not in settings.INSTALLED_APPS
        verbose_name = "Token"
        verbose_name_plural = "Tokens"

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super().save(*args, **kwargs)

    @classmethod
    def generate_key(cls):
        return binascii.hexlify(os.urandom(20)).decode()

    def __str__(self):
        return self.key



