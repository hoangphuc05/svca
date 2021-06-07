from rest_framework.authentication import TokenAuthentication
from members.models import CustomToken


class CustomTokenAuthorization(TokenAuthentication):
    model = CustomToken
