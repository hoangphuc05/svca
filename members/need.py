from rest_framework.decorators import api_view, permission_classes
from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from django.http import HttpResponse, JsonResponse
from django.utils import timezone

from members.models import ReactNeed, ReactVulnerableGroup


def querydict_to_dict(query_dict):
    data = {}
    for key in query_dict.keys():
        v = query_dict.getlist(key)
        if len(v) == 1:
            v = v[0]
        data[key] = v
        print("v: ", v)
        print("data: ", data)
    return data


@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def need_submit(request):
    data = querydict_to_dict(request.data)
    print(data)
    print(request.data)

    if data['first-name'] and data['last-name'] and data['need']:
        # create the need object
        need = ReactNeed(first_name=data['first-name'], last_name=data['last-name'], phone=data['phone'],
                         email=data['email'], address=data['address'], contact_reference=data['contact-preference'],
                         gender=data['gender'], ethnicity=data['ethnicity'], relationship=data['relationship'],
                         family18=data['0-18'], family19=data['19-54'], family55=data['55'],
                         language=data['language'], needs=data['need'], date=timezone.now(), )
        need.save()
        print('need saved')
        if 'vuln-group' in data:
            temp_data = [data['vuln-group']] if isinstance(data['vuln-group'], str) else data['vuln-group'] # convert to a list if it is not
            for vuln_group in temp_data:
                group, created = ReactVulnerableGroup.objects.get_or_create(name=str(vuln_group))
                need.vulnerable_groups.add(group)
    return HttpResponse(status=200)
