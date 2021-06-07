from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from rest_framework.decorators import api_view, permission_classes
from django.http import HttpResponse, JsonResponse
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, BasePermission, SAFE_METHODS

from members.models import CustomToken
from members import serializers
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
            response['successful'] = 1
            response['token'] = str(token)

        else:
            response['successful'] = 0
            response['token'] = ''

        return JsonResponse(response)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_signup(request):
    username = request.POST.get('username', None)
    password = request.POST.get('password', None)
    first_name = request.POST.get('first_name', "")
    last_name = request.POST.get('last_name', "")
    email = request.POST.get('email', "")
    response = {}
    if username and password:
        user = User.objects.create(username=username, password=password, first_name=first_name, last_name=last_name,
                                   email=email)
        user.save()
        response['successful'] = 1
        return JsonResponse(response)
    else:
        response['successful'] = 0
        return JsonResponse(response)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_signup(request):
    username = request.POST.get('username', None)
    password = request.POST.get('password', None)
    first_name = request.POST.get('first_name', "")
    last_name = request.POST.get('last_name', "")
    email = request.POST.get('email', "")
    response = {}
    if username and password:
        user = User.objects.create(username=username, password=password, first_name=first_name, last_name=last_name,
                                   email=email)
        user.save()
        response['successful'] = 1
        return JsonResponse(response)
    else:
        response['successful'] = 0
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
@permission_classes([IsAuthenticated])
# this is use to log out from other devices
def log_out_remote(request):
    user_id = request.user.id
    remote_token = request.POST.get('token', None)
    if remote_token:
        try:
            other_login = CustomToken.objects.get(user_id=user_id, key=remote_token)
        except CustomToken.DoesNotExist:
            raise PermissionDenied("You have no such token.")

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_devices(request):
    devices = []
    all_devices = CustomToken.objects.filter(user_id=request.user.id)
    serializer = serializers.CustomTokenSerializer(all_devices, many=True)
    return JsonResponse(serializer.data, safe=False)

# user = authenticate(username='john', password='secret')
# if user is not None:
#     # A backend authenticated the credentials
# else:
#     # No backend authenticated the credentials
