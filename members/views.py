from django.contrib.auth.models import User, Group
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework import permissions
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
                        'ethnicity', 'relationship', 'language', 'vulnerable_groups', 'needs', 'date', 'state']


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
    filterset_fields = ['id', 'assessment', 'date', 'author']


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
