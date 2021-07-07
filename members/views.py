from django.contrib.auth.models import User, Group
from django.http import HttpResponse
from rest_framework import viewsets, status
from rest_framework import generics
from rest_framework import permissions
from rest_framework.status import HTTP_400_BAD_REQUEST

from .serializers import ReactMemberSerializer, ReactNeedFullSerializer, ReactNeedSummarySerializer, ReactNeedWorkingSerializer, ReactFollowUpSerializer
from . import serializers
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, BasePermission, SAFE_METHODS, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

#custom permission group
from members import permission

from . import models


class PostOnlyPermissions(BasePermission):
    def has_permission(self, request, view):
        return request.method in ('POST',)


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class ReactMemberViewSet(viewsets.ModelViewSet):
    permission_classes = [permission.IsAdmin|PostOnlyPermissions]
    queryset = models.ReactMember.objects.all()
    serializer_class = ReactMemberSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'name']

    # def get(self, request, format=None):
    #     return Response('a')

class ReactNeedFullViewSet(viewsets.ModelViewSet):
    permission_classes = [permission.IsMember|PostOnlyPermissions]
    queryset = models.ReactNeed.objects.all()
    serializer_class = ReactNeedFullSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'first_name', 'last_name', 'phone', 'email', 'address', 'contact_reference', 'gender',
                        'ethnicity', 'relationship', 'language', 'vulnerable_groups', 'needs', 'date', 'state',
                        'family18', 'family19', 'family55']


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
                return Response({"old_password": ["Wrong password."]}, status=HTTP_400_BAD_REQUEST)
            # set the password
            new_password = serializer.data.get('new_password')
            repeat_password = serializer.data.get('repeat_new_password')
            if new_password != repeat_password:
                return Response({"new_password": ["Password not matching"]}, status=HTTP_400_BAD_REQUEST)
            self.object.set_password(new_password)
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password update successfully',

            }
            return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)