from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response

from . import models
from . import serializers
from members import permission

# Create your views here.


class PostViewSet(viewsets.ModelViewSet):
    queryset = models.Post.objects.all()
    serializer_class = serializers.PostSerializer

    def get_queryset(self):
        # https://stackoverflow.com/questions/45155867/dynamic-queryset-based-on-current-user
        if self.request.user.is_authenticated and self.request.user.groups.filter(name="is_site_editor").exists():
            return models.Post.objects.all()
        else:
            return models.Post.objects.filter(public=True)

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
            new_post = models.Post.objects.create(title=custom_serializer.data.get('title'), author=request.user)
            new_post.save()
            serializer = self.get_serializer(new_post)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class PostContentViewSet(viewsets.ModelViewSet):
    queryset = models.PostContent.objects.all()
    serializer_class = serializers.PostContentSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.groups.filter(name="is_site_editor").exists():
            return models.PostContent.objects.all()
        else:
            return models.PostContent.objects.filter(public=True)

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