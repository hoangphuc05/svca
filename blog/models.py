from django.db import models
from members import models as members_models

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True)
    author = models.ForeignKey(members_models.CustomUser, on_delete=models.SET_NULL, null=True, editable=False)
    url = models.CharField(max_length=255, null=True, unique=True)
    created_date = models.DateTimeField(auto_now_add=True)
    cover = models.URLField(null=True)
    public = models.BooleanField(default=False)


class PostContent(models.Model):
    # post = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True, unique=True)
    post = models.OneToOneField(Post, null=True, on_delete=models.SET_NULL)
    content = models.JSONField(blank=True)
    edit_date = models.DateTimeField(auto_now=True)
    edit_author = models.ForeignKey(members_models.CustomUser, on_delete=models.SET_NULL, null=True)
    public = models.BooleanField(default=False)


class ImageUpload(models.Model):
    image = models.ImageField(upload_to='uploads/')
