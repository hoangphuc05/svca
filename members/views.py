from pprint import pprint

from django.contrib.auth.models import User, Group
from django.http import HttpResponse, JsonResponse
from rest_framework import viewsets, status
from rest_framework import generics
from django.contrib.auth.decorators import login_required

from rest_framework.status import HTTP_400_BAD_REQUEST

from .models import CustomToken
from .serializers import ReactMemberSerializer, ReactNeedFullSerializer, ReactNeedSummarySerializer, ReactNeedWorkingSerializer, ReactFollowUpSerializer
from . import serializers
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import api_view, permission_classes

from rest_framework.permissions import IsAuthenticated, BasePermission, SAFE_METHODS, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

#custom permission group
from members import permission

from . import models, custom_paginator


class PostOnlyPermissions(BasePermission):
    def has_permission(self, request, view):
        return request.method in ('POST',)


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [permission.IsSuperUser]
    queryset = models.CustomUser.objects.all()
    serializer_class = serializers.UserSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'first_name', 'last_name', 'username', 'groups', 'email']


class ReactMemberViewSet(viewsets.ModelViewSet):
    permission_classes = [permission.IsAdmin|PostOnlyPermissions]
    queryset = models.ReactMember.objects.all()
    serializer_class = ReactMemberSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'name', 'accepted']

    # def get(self, request, format=None):
    #     return Response('a')

class ReactNeedFullViewSet(viewsets.ModelViewSet):
    permission_classes = [permission.IsAdmin|PostOnlyPermissions]
    queryset = models.ReactNeed.objects.all()
    serializer_class = ReactNeedFullSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'first_name', 'last_name', 'phone', 'email', 'address', 'contact_reference', 'gender',
                        'ethnicity', 'relationship', 'language', 'vulnerable_groups', 'housing', 'needs', 'date', 'state',
                        'family18', 'family19', 'family55']

    # def create(self, request, *args, **kwargs):
    #
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #
    #     # overwrite state
    #     custom_validated = serializer.validated_data
    #     # print()
    #     custom_validated['state'] = 0
    #     vulnerable_groups = custom_validated.pop('vulnerable_groups')
    #     new_need = models.ReactNeed.objects.create(**custom_validated)
    #     new_need.save()
    #     for vuln in vulnerable_groups:
    #         vuln_obj, created = models.ReactVulnerableGroup.objects.get_or_create(name=vuln.name)
    #         new_need.vulnerable_groups.add(vuln_obj)
    #
    #     # self.perform_create(serializer)
    #     headers = self.get_success_headers(self.get_serializer(new_need).data)
    #     return Response(self.get_serializer(new_need).data, status=status.HTTP_201_CREATED, headers=headers)
    #
    # def partial_update(self, request, *args, **kwargs):
    #
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance, data=request.data, partial=True)
    #     serializer.is_valid(raise_exception=True)
    #     # print(serializer.validated_data);
    #
    #     serializer.save()
    #     return Response(serializer.data)



# class ReactNeedUpdateViewSet(viewsets.ModelViewSet):
#     permission_classes = [permission.IsMember|PostOnlyPermissions]
#     queryset = models.ReactNeed.objects.all()
#     serializer_class = serializers.ReactNeedFullUpdateSerializer
#     filter_backends = [DjangoFilterBackend]
#     filterset_fields = ['id', 'first_name', 'last_name', 'phone', 'email', 'address', 'contact_reference', 'gender',
#                         'ethnicity', 'relationship', 'language', 'vulnerable_groups', 'needs', 'date', 'state',
#                         'family18', 'family19', 'family55']


class ReactNeedSummaryViewSet(viewsets.ModelViewSet):
    permission_classes = [permission.IsMember|PostOnlyPermissions]
    queryset = models.ReactNeed.objects.all()
    serializer_class = ReactNeedSummarySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'first_name', 'last_name', 'phone', 'email', 'contact_reference', 'gender',
                        'language', 'vulnerable_groups', 'needs', 'date']


class ReactNeedWorkingViewSet(viewsets.ModelViewSet):
    permission_classes = [permission.IsAdmin]
    queryset = models.ReactNeedWorking.objects.all()
    serializer_class = ReactNeedWorkingSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'agency', 'response']


class ReactNeedAssessmentViewSet(viewsets.ModelViewSet):
    permission_classes = [permission.IsAdmin]
    queryset = models.ReactNeedAssessment.objects.all()
    serializer_class = serializers.ReactNeedAssessmentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'assessment', 'date', 'author', 'response']


class ReactFollowUpViewSet(viewsets.ModelViewSet):
    permission_classes =[permission.IsAdmin]
    queryset = models.ReactFollowUp.objects.all()
    serializer_class = ReactFollowUpSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'worker', 'date', 'response']



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reactMemberConfirmViewSet(request, member_id):
    member = get_object_or_404(models.ReactMember, pk=member_id)
    member.accepted = 1
    member.save()
    return HttpResponse(str(member.accepted))

# https://stackoverflow.com/questions/27592513/basic-django-rest-framework-write-only-resource

class UserSignup(generics.CreateAPIView):
    """
    Endpoint for creating new user
    """
    serializer_class = serializers.UserSignupSerializers
    model = models.CustomUser

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            new_user = models.CustomUser.objects.create_user(username=serializer.data.get('username'),
                                                             email=serializer.data.get('email'),
                                                             password=serializer.data.get('password'))
            new_user.first_name = serializer.data.get('first_name')
            new_user.last_name = serializer.data.get('last_name')
            new_user.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'detail': 'Account create successfully',
            }
            return Response(response)
        return Response(serializer.errors, status= HTTP_400_BAD_REQUEST)

class UserGroupUpdate(generics.UpdateAPIView):
    """
    Endpoint for updating user's group
    """
    serializer_class = serializers.UserGroupUpdateSerializers
    model = models.CustomUser
    permission_classes(permission.IsSuperUser)

    queryset = models.CustomUser.objects.all()

    def get_object(self):
        request = self.request
        serializer = self.get_serializer(data=request.data)
        queryset = self.filter_queryset(self.get_queryset())
        # make sure to catch 404's below
        if serializer.is_valid():
            user = get_object_or_404(models.CustomUser, username=serializer.data.get('username'))
            # user = models.CustomUser.objects.get(username=serializer.data.get('username'))
            return user
        return HTTP_400_BAD_REQUEST

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = models.CustomUser.objects.get(username=serializer.data.get('username'))

            # remove user from all group to prepare to update
            user.groups.clear()
            print(user.groups)
            # pprint(serializer.data.get('groups'))
            for group in serializer.data.get('groups'):
                new_group, created = Group.objects.get_or_create(name=group)
                user.groups.add(new_group)
                # print(group)
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'detail': 'Account update successfully',
            }
            return Response(response)


class GetDevices(generics.GenericAPIView):
    # serializer_class
    permission_classes = [IsAuthenticated]
    pagination_class = custom_paginator.CustomPageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'devices', 'created']
    # ordering_fields = ['id', 'devices', 'created']
    queryset = CustomToken.objects.all()
    def get(self, request, format=None):
        '''
        Return all token of the user
        :param request:
        :param format:
        :return:
        '''
        queryset = CustomToken.objects.filter(user_id=request.user.id)
        page = self.request.query_params.get('page', 1)
        if page is not None:
            paginated_devices = self.paginate_queryset(queryset)
            serializer = serializers.CustomTokenSerializer(paginated_devices, many=True)
            # return JsonResponse(self.get_paginated_response(serializer.data), safe=False)
            return self.get_paginated_response(serializer.data)

        serializer = serializers.CustomTokenSerializer(queryset, many=True)
        return JsonResponse(serializer.data, safe=False)



class ChangePasswordView(generics.UpdateAPIView):
    """
    Endpoint for changing password
    """
    serializer_class = serializers.ChangePasswordSerializers
    model = models.CustomUser
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset = None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # check old password
            if not self.object.check_password(serializer.data.get('old_password')):
                return Response({"detail": ["Wrong old password."]}, status=HTTP_400_BAD_REQUEST)
            # set the password
            new_password = serializer.data.get('new_password')
            repeat_password = serializer.data.get('repeat_new_password')
            if new_password != repeat_password:
                return Response({"detail": ["New password is not matching"]}, status=HTTP_400_BAD_REQUEST)
            self.object.set_password(new_password)
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'detail': 'Password update successfully',

            }
            return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)