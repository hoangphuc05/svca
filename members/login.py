import requests
from django.contrib.auth import authenticate
from django.contrib.auth.models import User, Group
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from rest_framework.decorators import api_view, permission_classes, parser_classes
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import IsAuthenticated, BasePermission, SAFE_METHODS
from django.forms.models import model_to_dict
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from django.conf import settings
from rest_framework import pagination
from rest_framework import generics
# from django.shortcuts import get_object_or_404

# custom permission group
from members import permission

from members.models import CustomToken
from members import serializers
from members.models import CustomUser, ReactMember
import json
from . import custom_paginator


def verify_captcha(captcha_token):
    url = "https://www.google.com/recaptcha/api/siteverify"
    data = {
        'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
        'response': captcha_token
    }
    r = requests.post(url=url, data=data)
    response_dict = json.loads(r.text)
    return response_dict['success']


@api_view(['POST'])
@parser_classes([JSONParser, FormParser, MultiPartParser])
def user_login(request):
    response = {}
    username = request.data.get('username', None)
    password = request.data.get('password', None)
    device_info = request.data.get('device', None)
    token = request.data.get('token', None)

    if not verify_captcha(token):
        return JsonResponse({'detail': 'ReCaptcha is invalid'}, status=401)

    if username and password:
        user = authenticate(username=str(request.POST['username']), password=str(request.POST['password']))

        if user is not None:
            token = CustomToken.objects.create(user=user, devices=device_info)
            response['status'] = 1
            response['token'] = str(token)
        else:
            response['status'] = 0
            response['token'] = ''
            return JsonResponse(response, status=401)
        return JsonResponse(response)


# MeoRung_member:mr123
@api_view(['POST'])
def member_signup(request):
    # This sign up is for new member after finishing the form and should be public

    # each account need to associate with a member
    # get the member id
    member_id = request.POST.get('member_id', None)
    email = request.POST.get('email', None)
    password = request.POST.get('password', None)
    repeatPassword = request.POST.get('repeatpass', None)
    response = {}
    if email and password and repeatPassword == password:
        # get the member profile from the member id
        try:
            member_profile = ReactMember.objects.get(id=member_id)
            if member_profile.account is not None:
                return JsonResponse({"error": "Member already have an account"}, status=403)
        except ObjectDoesNotExist:
            return JsonResponse({"error": "No member found"}, status=404)
        # get the group
        group, created = Group.objects.get_or_create(name="is_member")
        user = CustomUser.objects.create_user(username=email, password=password, first_name=member_profile.name,
                                              last_name=member_profile.name,
                                              email=member_profile.email)
        user.save()
        user.groups.add(group)

        # add relationship of the member profile to the new registered user
        member_profile.account = user
        member_profile.save()
        response['status'] = 1
        return JsonResponse(response)
    else:
        response['status'] = 0
        return JsonResponse(response, status=400)


# This view is for user signing up a new account
@api_view(['POST'])
@parser_classes([JSONParser, FormParser, MultiPartParser])
def user_signup(request):

    # this sign up can be access publicly but no permission given
    username = request.data.get('email', None)
    password = request.data.get('password', None)
    repeatPassword = request.data.get('confirm', None)
    first_name = request.data.get('first_name', "")
    last_name = request.data.get('last_name', "")
    email = request.data.get('email', "")
    token = request.data.get('token', None)
    response = {}
    if not verify_captcha(token):
        return JsonResponse({'detail': 'ReCaptcha is invalid'}, status=401)
    if email and len(CustomUser.objects.filter(email=email)) > 0:
        return JsonResponse({'detail': 'Email already registered'}, status=401)
    if username and email and password and repeatPassword == password:
        user = CustomUser.objects.create_user(username=username, password=password, first_name=first_name,
                                              last_name=last_name,
                                              email=email)
        user.save()
        response['status'] = 1
        return JsonResponse(response)
    else:
        response['status'] = 0
        return JsonResponse({'detail': 'Missing information'}, status=401)


@api_view(['GET'])
@login_required
@permission_classes([IsAuthenticated])
def get_authenticated(request):
    user = request.user
    response = {}
    response = model_to_dict(user, fields=['id', 'username', 'first_name', 'last_name', 'email'])
    response['authenticated'] = 1
    return JsonResponse(response)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def log_out(request):
    try:
        request.auth.delete()
        return HttpResponse(status=200)
    except:
        return HttpResponse(status=500)
    # return HttpResponse(str(request.auth.key))


@api_view(['POST'])
@parser_classes([JSONParser, FormParser, MultiPartParser])
# @permission_classes([IsAuthenticated])
# this is use to log out from other devices
def remove_device(request):
    user_id = request.user.id
    id = request.data.get('tokenid',-1)
    # id = request.POST.get('tokenid', None)
    if id:
        try:
            other_login = CustomToken.objects.get(user_id=user_id, id=id)
            other_login.delete()
            return HttpResponse(status=204)
        except CustomToken.DoesNotExist:
            raise PermissionDenied("You have no such token.")


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_devices(request):
    devices = []
    all_devices = CustomToken.objects.filter(user_id=request.user.id)
    serializer = serializers.CustomTokenSerializer(all_devices, many=True)
    pagination = custom_paginator.CustomPageNumberPagination

    return JsonResponse(serializer.data, safe=False)





@api_view(['POST'])
def change_password(request):
    response = {}
    username = request.POST.get('username', None)
    password = request.POST.get('password', None)
    new_password = request.POST.get('new_password', None)
    if username and password and new_password:
        user = authenticate(username=str(request.POST['username']), password=str(request.POST['password']))

        if user is not None:
            user.set_password(new_password)
            user.save()

        else:
            response['status'] = 0
            response['error'] = 'Unable to authenticate'
            return JsonResponse(response, status=401)

    return JsonResponse(response)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_all(request):
    """
    Log out of all device by deleting all token accept the one used to make the request.
    :param reqeust:
    :return:
    """
    if request.auth is not None and request.user is not None:
        all_other_token = CustomToken.objects.filter(user=request.user).exclude(id=request.auth.id).delete()
        return HttpResponse(status=204)
    return HttpResponse(status=401)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([JSONParser, FormParser, MultiPartParser])
def check_permission(request):
    perm = request.data.get('permission', None)
    if perm is not None:
        if request.user.groups.filter(name=perm).exists():
            return HttpResponse(status=204)
        return HttpResponse(status=401)
    return HttpResponse(status=400)


class ListPermission(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    # serializer_class = serializers.GroupSerializer

    def get_object(self):
        return self.request.user

    def get(self, request, *args, **kwargs):
        object = self.get_object()
        serializer = serializers.UserInfo(object)
        return JsonResponse(serializer.data, safe=False)

# user = authenticate(username='john', password='secret')
# if user is not None:
#     # A backend authenticated the credentials
# else:
#     # No backend authenticated the credentials


