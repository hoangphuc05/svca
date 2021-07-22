from django.db import models
from members import models as members_models

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(members_models.CustomUser, on_delete=models.SET_NULL, null=True, editable=False)
    url = models.CharField(max_length=255)
    created_date = models.DateTimeField(auto_now_add=True)
    public = models.BooleanField(default=False)


class PostContent(models.Model):
    post = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True)
    content = models.JSONField(blank=True)
    edit_date = models.DateTimeField(auto_now=True)
    edit_author = models.ForeignKey(members_models.CustomUser, on_delete=models.SET_NULL, null=True)
    public = models.BooleanField(default=False)

