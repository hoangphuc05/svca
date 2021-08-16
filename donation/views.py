from django.shortcuts import render
from rest_framework.decorators import api_view, parser_classes, permission_classes
from rest_framework.parsers import FormParser, JSONParser
from rest_framework.response import Response
from django.utils import timezone
import requests
from requests.auth import HTTPBasicAuth
import datetime
import urllib.parse

from members import permission
from donation import models

import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
print(dotenv_path)
load_dotenv(dotenv_path)

paypal_base_url = os.getenv("PAYPAL_BASE_URL")

# Create your views here.

# def validate_ipn(request_content):
#     headers = {'content-type': 'application/x-www-form-urlencoded',
#                'user-agent': 'Python-IPN-Verification-Script'}
#     request_content.update({'cmd': '_notify-validate'})
#     url_test = 'https://enq0b7m3rqb7oej.m.pipedream.net'
#     url_sandbox = 'https://ipnpb.sandbox.paypal.com/cgi-bin/webscr'
#     r = requests.post(url_sandbox, data=request_content, headers=headers)
#     r.raise_for_status()
#
#     # if r.text == 'VERIFIED':
#     #     print()
#     # elif r.text == 'INVALID':
#     #     pass
#     # else:
#     #     pass
#     # print(r.text)
#     r = requests.post(url_test, data=request_content, headers=headers)
#
#     return


# @api_view(['POST'])
# @parser_classes([FormParser])
# def ipn_listener(request):
#     ipn_message = request.data.dict()
#     # ipn_message.update({'cmd': '_notify-validate'})
#     validate_ipn(ipn_message)
#     print(ipn_message)
#     return Response(status=200)





# def handle_webhook(request_content):
#     headers = {'Content-Type': 'application/json',
#                'user-agent': 'Python-IPN-Verification-Script'}
#     url_test = 'https://enq0b7m3rqb7oej.m.pipedream.net'
#     r = requests.post(url_test, data=request_content, headers=headers)
#     return


# @api_view(['POST'])
# @parser_classes([JSONParser])
# def webhook_listener(request):
#     webhook_data = request.data.dict()
#     handle_webhook(webhook_data)
#     return Response(status=200)


def get_token_object():
    print("new token method called")
    sandbox_url = f"{paypal_base_url}/v1/oauth2/token"
    body = {"grant_type": "client_credentials"}
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    client_id = os.getenv("PAYPAL_CLIENT_ID")
    client_secret = os.getenv("PAYPAL_CLIENT_SECRET")

    r = requests.post(sandbox_url, data=body, auth=HTTPBasicAuth(client_id, client_secret))
    r.raise_for_status()
    return r.json()


def get_transaction_list(token):
    url = f"{paypal_base_url}/v1/reporting/transactions"
    headers = {"Authorization": f"Bearer {token}"}
    params = {"start_date": (datetime.datetime.utcnow() - datetime.timedelta(days=30)).isoformat()[:-7]+'Z',
              "end_date": datetime.datetime.utcnow().isoformat()[:-7]+'Z',
              "fields": "all",
              # "transaction_status": "S", # search for success transaction only
              "page_size": 500,
              "transaction_type": "T0013"} # search for donation only
    params_str = urllib.parse.urlencode(params, safe=':+')
    r = requests.get(url, headers=headers, params=params_str)
    r.raise_for_status()
    return r.json()


def transaction_info_builder(response):
    transaction_info = {'last_refreshed_datetime': response['last_refreshed_datetime'],
                        'transaction_details': response['transaction_details'],
                        'total_items': response['total_items'],
                        'total_pages': response['total_pages']}
    return transaction_info

# flat our the transaction data from PayPal to a simple list
# def transaction_data_convert(data):
#     for transaction in data['transaction_details']:
#         transaction_data = {}
#         transaction_data['']


@api_view(['GET'])
@permission_classes([permission.IsAdmin])
def list_transaction(request):
    # try to get the access token, if the result is None then create a new one
    access_token = None
    try:
        token_object = models.PaypalToken.objects.get(app_id=os.getenv('PAYPAL_APP_ID'))
        access_token = token_object.validate_token()
    except models.PaypalToken.DoesNotExist:
        # no token found, set access_token to False
        access_token = None

    # if access token is none then create a new one
    if access_token is None:
        token_response = get_token_object()
        # create a new token object
        new_token = models.PaypalToken(scope=token_response['scope'], access_token=token_response['access_token'],
                                       app_id=token_response['app_id'],
                                       expire_time=timezone.now() +
                                                   datetime.timedelta(seconds=int(token_response['expires_in'])))
        new_token.save()
        # get access token from new token
        access_token = new_token.validate_token()
    # get the list of donation transaction
    transaction_data = transaction_info_builder(get_transaction_list(access_token))
    return Response(data=transaction_data, status=200)