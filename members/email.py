import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
import os
import html2text
from dotenv import load_dotenv
from django.dispatch import receiver
from django.urls import reverse

from django_rest_passwordreset.signals import reset_password_token_created

dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
print(dotenv_path)
load_dotenv(dotenv_path)


api_key = os.getenv('EMAIL_TOKEN')
configuration = sib_api_v3_sdk.Configuration()
configuration.api_key['api-key'] = api_key

api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))


@receiver(reset_password_token_created)
def email_reset_password(sender, instance, reset_password_token, *args, **kwargs):
    to = [{"email": reset_password_token.user.email, "name": reset_password_token.user.first_name + " " + reset_password_token.user.last_name}]
    params = {"RESET_URL": "{}?token={}".format(
            instance.request.build_absolute_uri(reverse('members:password_reset:reset-password-confirm')),
            reset_password_token.key)
    }
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=to, params=params)
    try:
        api_response = api_instance.send_transac_email(send_smtp_email)
    except ApiException as e:
        print("Exception when calling SMTPApi->send_transac_email: %s\n" % e)



