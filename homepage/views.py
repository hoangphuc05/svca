from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets, status
from rest_framework import generics
from rest_framework import permissions
from . import models, serializers
from django_filters.rest_framework import DjangoFilterBackend


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


from members.permission import IsSiteEditor


# Create your views here.





class SiteInfoViewset(viewsets.ModelViewSet):
    permission_classes = [IsSiteEditor | ReadOnly]
    queryset = models.SiteInfo.objects.all()
    serializer_class = serializers.SiteInfoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["id", "name"]


