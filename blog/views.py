from pprint import pprint

from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from django.http import HttpResponse, JsonResponse

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser

from . import models
from . import serializers
from members import permission, custom_paginator

# Create your views here.


class PostViewSet(viewsets.ModelViewSet):
    queryset = models.Post.objects.all()
    serializer_class = serializers.PostSerializer
    pagination_class = custom_paginator.CustomPageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'url']

    def get_queryset(self):
        # https://stackoverflow.com/questions/45155867/dynamic-queryset-based-on-current-user
        if self.request.user.is_authenticated and self.request.user.groups.filter(name="is_site_editor").exists():
            return models.Post.objects.all().order_by('-id')
        else:
            return models.Post.objects.filter(public=True).order_by('-id')

    # def get_object(self):
    #     pprint(self.kwargs)
    #     return self.get_queryset().get(pk=self.kwargs['pk'])

    def get_permissions(self):
        """
        :return: List of permission based on what action
        """
        if self.action in ["list", "retrieve"]:
            permission_classes = []
        else:
            permission_classes = [permission.IsSiteEditor]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        # serializer = self.get_serializer(data=request.data)
        serializer = None
        custom_serializer = serializers.CreatePostSerializer(data=request.data)
        if custom_serializer.is_valid(raise_exception=True):
            # new_post = models.Post.objects.create(title=custom_serializer.data.get('title'), author=request.user)
            new_post = models.Post.objects.create(author=request.user, **custom_serializer.validated_data)
            new_post.save()

            serializer = self.get_serializer(new_post)
            # serializer.is_valid()
            # self.queryset = new_post
            # self.perform_update(custom_serializer.validated_data)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # def retrieve(self, request, *args, **kwargs):


class PostContentViewSet(viewsets.ModelViewSet):
    queryset = models.PostContent.objects.all()
    serializer_class = serializers.PostContentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'post']

    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.groups.filter(name="is_site_editor").exists():
            return models.PostContent.objects.all()
        else:
            # return models.Post.objects.filter(public=True).
            return models.PostContent.objects.filter(post__in=models.Post.objects.filter(public=True))

    def get_permissions(self):
        """
        :return: List of permission based on what action
        """
        if self.action in ["list", "retrieve"]:
            permission_classes = []
        else:
            permission_classes = [permission.IsSiteEditor]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        # serializer = self.get_serializer(data=request.data)
        serializer = None
        custom_serializer = serializers.CreatePostContentSerializer(data=request.data)
        if custom_serializer.is_valid(raise_exception=True):
            new_post = models.PostContent.objects.create(post=models.Post.objects.get(pk=custom_serializer.data.get('post')), content=custom_serializer.data.get('content'), edit_author=request.user)
            new_post.save()
            serializer = self.get_serializer(new_post)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ImageUploadViewset(viewsets.ModelViewSet):
    queryset = models.ImageUpload.objects.all()
    serializer_class = serializers.ImageUploadSerializer
    parser_classes = [MultiPartParser]

    def create(self, request, *args, **kwargs):
        print(request.data)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        # return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response({
            'success': 1,
            'file': {
                "url": list(serializer.data.values())[0],  # why tf do I need to do so many convert???
            }
        })