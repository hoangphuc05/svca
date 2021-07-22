from django.db import models
from members import models as members_models

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(members_models.CustomUser, on_delete=models.SET_NULL, null=True)


class PostContent(models.Model):
    post = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True)
    content = models.JSONField()
