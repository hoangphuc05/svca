from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes
from django.http import HttpResponse, JsonResponse
from rest_framework.authtoken.models import Token
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

# @api_view(['POST'])
# def user_signup(request):



# user = authenticate(username='john', password='secret')
# if user is not None:
#     # A backend authenticated the credentials
# else:
#     # No backend authenticated the credentials