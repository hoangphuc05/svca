from django.shortcuts import render
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import FormParser
from rest_framework.response import Response
import requests

# Create your views here.

def validate_ipn(request_content):
    headers = {'content-type': 'application/x-www-form-urlencoded',
               'user-agent': 'Python-IPN-Verification-Script'}
    request_content.update({'cmd': '_notify-validate'})
    url_test = 'https://enq0b7m3rqb7oej.m.pipedream.net'
    url_sandbox = 'https://ipnpb.sandbox.paypal.com/cgi-bin/webscr'
    r = requests.post(url_sandbox, data=request_content, headers=headers)
    r.raise_for_status()

    # if r.text == 'VERIFIED':
    #     print()
    # elif r.text == 'INVALID':
    #     pass
    # else:
    #     pass
    # print(r.text)
    r = requests.post(url_test, data=request_content, headers=headers)

    return


@api_view(['POST'])
@parser_classes([FormParser])
def ipn_listener(request):
    ipn_message = request.data.dict()
    # ipn_message.update({'cmd': '_notify-validate'})
    validate_ipn(ipn_message)
    print(ipn_message)
    return Response(status=200)
