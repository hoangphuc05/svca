from rest_framework import serializers
from . import models


class PostSerializer(serializers.ModelSerializer):
    """
    Serializers for post table
    """
    class Meta:
        model = models.Post
        fields = ['id', 'title', 'author', 'url', 'created_date', 'public']


class CreatePostSerializer(serializers.Serializer):
    model = models.Post
    title = serializers.CharField(required=True)
    public = serializers.BooleanField(default=False)


class PostContentSerializer(serializers.ModelSerializer):
    """
    Serializers for post content
    """
    class Meta:
        model = models.PostContent
        fields = ['id', 'post', 'content', 'edit_author', 'public']


class CreatePostContentSerializer(serializers.Serializer):
    model = models.PostContent
    post = serializers.PrimaryKeyRelatedField(queryset=models.Post.objects.all())
    content = serializers.JSONField(required=True)
    public = serializers.BooleanField(default=False)

