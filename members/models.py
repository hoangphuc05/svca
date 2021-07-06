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



# class AuthGroup(models.Model):
#     name = models.CharField(unique=True, max_length=150)
#
#     class Meta:
#         managed = False
#         db_table = 'auth_group'


# class AuthGroupPermissions(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
#     permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)
#
#     class Meta:
#         managed = False
#         db_table = 'auth_group_permissions'
#         unique_together = (('group', 'permission'),)
#

# class AuthPermission(models.Model):
#     name = models.CharField(max_length=255)
#     content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
#     codename = models.CharField(max_length=100)
#
#     class Meta:
#         managed = False
#         db_table = 'auth_permission'
#         unique_together = (('content_type', 'codename'),)


# class AuthUser(models.Model):
#     password = models.CharField(max_length=128)
#     last_login = models.DateTimeField(blank=True, null=True)
#     is_superuser = models.IntegerField()
#     username = models.CharField(unique=True, max_length=150)
#     first_name = models.CharField(max_length=150)
#     last_name = models.CharField(max_length=150)
#     email = models.CharField(max_length=254)
#     is_staff = models.IntegerField()
#     is_active = models.IntegerField()
#     date_joined = models.DateTimeField()
#
#     class Meta:
#         managed = False
#         db_table = 'auth_user'


# class AuthUserGroups(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     user = models.ForeignKey(AuthUser, models.DO_NOTHING)
#     group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
#
#     class Meta:
#         managed = False
#         db_table = 'auth_user_groups'
#         unique_together = (('user', 'group'),)


# class AuthUserUserPermissions(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     user = models.ForeignKey(AuthUser, models.DO_NOTHING)
#     permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)
#
#     class Meta:
#         managed = True
#         db_table = 'auth_user_user_permissions'
#         unique_together = (('user', 'permission'),)


# class BlogOption(models.Model):
#     option_name = models.CharField(max_length=255)
#     option_value = models.TextField()
#
#     class Meta:
#         managed = True
#         db_table = 'blog_option'


# class Category(models.Model):
#     name = models.CharField(max_length=255)
#
#     class Meta:
#         managed = True
#         db_table = 'category'
#
#
# class CategoryRelationship(models.Model):
#     post = models.OneToOneField('Post', models.DO_NOTHING, primary_key=True)
#     category = models.ForeignKey(Category, models.DO_NOTHING)
#
#     class Meta:
#         managed = False
#         db_table = 'category_relationship'
#         unique_together = (('post', 'category'),)


# class Comment(models.Model):
#     author = models.ForeignKey('User', models.DO_NOTHING)
#     post = models.ForeignKey('Post', models.DO_NOTHING)
#     parent_comment_id = models.IntegerField(blank=True, null=True)
#     date = models.DateTimeField()
#     modified_date = models.DateTimeField(blank=True, null=True)
#     content = models.TextField()
#     status = models.IntegerField()
#
#     class Meta:
#         managed = False
#         db_table = 'comment'


# class CommentLike(models.Model):
#     comment = models.ForeignKey(Comment, models.DO_NOTHING)
#     user = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)
#     ip_address = models.CharField(max_length=45, blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'comment_like'


# class DjangoAdminLog(models.Model):
#     action_time = models.DateTimeField()
#     object_id = models.TextField(blank=True, null=True)
#     object_repr = models.CharField(max_length=200)
#     action_flag = models.PositiveSmallIntegerField()
#     change_message = models.TextField()
#     content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
#     user = models.ForeignKey(AuthUser, models.DO_NOTHING)
#
#     class Meta:
#         managed = False
#         db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Paragraph(models.Model):
    post_id = models.IntegerField(primary_key=True)
    paragraph_index = models.IntegerField()
    type = models.IntegerField()
    content = models.TextField()

    class Meta:
        managed = False
        db_table = 'paragraph'
        unique_together = (('post_id', 'paragraph_index'),)


class Post(models.Model):
    post_title = models.TextField()
    author = models.ForeignKey('User', models.DO_NOTHING)
    create_date = models.TextField()
    raw_post_content = models.TextField()
    modified_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'post'


class PostLike(models.Model):
    post = models.ForeignKey(Post, models.DO_NOTHING)
    user = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)
    ip_address = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'post_like'

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    pass

class ReactMember(models.Model):
    name = models.CharField(max_length=255)
    contact_name = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    contact_type = models.IntegerField()
    member_type = models.IntegerField()
    location_type = models.IntegerField()
    accepted = models.IntegerField(blank=True, null=True)
    account = models.OneToOneField(CustomUser, on_delete=models.SET_NULL, null=True)

    class Meta:
        managed = True
        db_table = 'react_member'
        permissions = [
            ("is_member", "Is a member and conly view specific information")
        ]


# class ReactVulnerableGroup(models.Model):
#     class Meta:
#         db_table = "react_vulnerable_group"
#     name = models.CharField(max_length=255)


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
    contact_reference = models.IntegerField(blank=True, null=True)
    gender = models.CharField(max_length=255, blank=True, null=True)
    ethnicity = models.CharField(max_length=255, blank=True, null=True)
    relationship = models.CharField(max_length=255, blank=True, null=True)
    language = models.CharField(max_length=255, blank=True, null=True)
    # vulnerable_groups = models.ManyToManyField(ReactVulnerableGroup)
    vulnerable_groups = models.ManyToManyField(ReactVulnerableGroup)
    family18 = models.IntegerField()
    family19 = models.IntegerField()
    family55 = models.IntegerField()
    needs = models.TextField()
    date = models.DateTimeField()
    state = models.IntegerField(null=True)

    def __str__(self):
        return '{self.first_name}'.format(self=self)


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

