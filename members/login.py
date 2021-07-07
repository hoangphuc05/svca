from django.contrib.auth import authenticate
from django.contrib.auth.models import User, Group
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from rest_framework.decorators import api_view, permission_classes, parser_classes
from django.http import HttpResponse, JsonResponse
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, BasePermission, SAFE_METHODS
from django.forms.models import model_to_dict
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
# from django.shortcuts import get_object_or_404

# custom permission group
from members import permission

from members.models import CustomToken
from members import serializers
from members.models import CustomUser, ReactMember
import json


@api_view(['POST'])
def user_login(request):
    response = {}
    username = request.POST.get('username', None)
    password = request.POST.get('password', None)
    device_info = request.POST.get('device', None)
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


# newMew:ww123
@api_view(['POST'])
def user_signup(request):
    # this sign up is for organization's member and should not be expose publicly
    username = request.POST.get('username', None)
    password = request.POST.get('password', None)
    repeatPassword = request.POST.get('repeatpass', None)
    first_name = request.POST.get('first_name', "")
    last_name = request.POST.get('last_name', "")
    email = request.POST.get('email', "")
    response = {}
    if username and password and repeatPassword == password:
        # get the group
        group, created = Group.objects.get_or_create(name="is_user")
        user = CustomUser.objects.create_user(username=username, password=password, first_name=first_name,
                                              last_name=last_name,
                                              email=email)
        user.save()
        user.groups.add(group)
        response['status'] = 1
        return JsonResponse(response)
    else:
        response['status'] = 0
        return JsonResponse(response)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_authenticated(request):
    user = request.user
    response = {}
    response = model_to_dict(user, fields=['username', 'first_name', 'last_name', 'email'])
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
# user = authenticate(username='john', password='secret')
# if user is not None:
#     # A backend authenticated the credentials
# else:
#     # No backend authenticated the credentials
