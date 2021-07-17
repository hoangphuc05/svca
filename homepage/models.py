from django.db import models

# Create your models here.


class SiteInfo(models.Model):
    """
    Class for storing information to display in the homepage.
    """
    name = models.CharField(max_length=255, unique=True)
    note = models.TextField(blank=True)
    value = models.TextField(blank=True)