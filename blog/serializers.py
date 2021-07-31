from rest_framework import serializers
from . import models


class PostSerializer(serializers.ModelSerializer):
    """
    Serializers for post table
    """
    author = serializers.StringRelatedField()
    class Meta:
        model = models.Post
        fields = ['id', 'title', 'description', 'author', 'url', 'created_date', 'cover', 'public']


class CreatePostSerializer(serializers.Serializer):
    model = models.Post
    title = serializers.CharField(required=True)
    public = serializers.BooleanField(required=False)
    description = serializers.CharField(required=False)
    url = serializers.CharField(required=False)
    cover = serializers.URLField(required=False)


class PostContentSerializer(serializers.ModelSerializer):
    """
    Serializers for post content
    """
    content = serializers.JSONField(default="")
    class Meta:
        model = models.PostContent
        fields = ['id', 'post', 'content', 'edit_author', 'public']


class CreatePostContentSerializer(serializers.Serializer):
    model = models.PostContent
    post = serializers.PrimaryKeyRelatedField(queryset=models.Post.objects.all())
    content = serializers.JSONField(default="")
    public = serializers.BooleanField(default=False)


class ImageUploadSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.ImageUpload
        fields = ['image']

