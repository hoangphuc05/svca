from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from django.http import HttpResponse, JsonResponse
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, BasePermission, SAFE_METHODS
import json


@api_view(['POST'])
def user_login(request):
    response = {}
    if request.POST['username'] and request.POST['password']:
        user = authenticate(username=str(request.POST['username']), password=str(request.POST['password']))

        if user is not None:
            token, create_new = Token.objects.get_or_create(user=user)
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
        user = User.objects.create(username=username, password=password, first_name=first_name, last_name=last_name, email=email)
        user.save()
        response['successful'] = 1
        return JsonResponse(response)
    else:
        response['successful'] = 0
        return JsonResponse(response)


# user = authenticate(username='john', password='secret')
# if user is not None:
#     # A backend authenticated the credentials
# else:
#     # No backend authenticated the credentials