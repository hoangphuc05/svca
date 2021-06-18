from rest_framework.decorators import api_view, permission_classes
from django.http import HttpResponse, JsonResponse
import json

from .email import send_an_email
from members import permission
@api_view(['POST'])
# @permission_classes([permission.IsAdmin])
def send_email(request):
    # get information
    # subject = request.POST.get('subject', None)
    # html_content = request.POST.get('html_content', None)
    # variables = request.POST.getlist('vars', None)
    # recipients = request.POST.getlist('recipients', None)
    # from_email = request.POST.get('from_email', 'no-reply@meorung.me')
    # from_name = request.POST.get('from_name', 'No Reply Meorung services')
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    subject = body.get('subject')
    html_content = body.get('html_content', None)
    variables = body.get('vars', None)
    recipients = body.get('recipients', None)
    from_email = body.get('from_email', 'no-reply@meorung.me')
    from_name = body.get('from_name', 'no-reply services')
    print(variables)
    if subject and html_content and recipients and from_name and from_email:
        print(recipients)
        send_an_email(subject, html_content, recipients, variables, from_email, from_name)
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=400)

