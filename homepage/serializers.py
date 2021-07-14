from rest_framework import serializers

from . import models

class SiteInfoSerializer(serializers.ModelSerializer):
    """
    Serializers for site info
    """
    class Meta:
        model = models.SiteInfo
        fields = ['id', 'name', 'value']
