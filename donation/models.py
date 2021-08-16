from django.db import models
import datetime
from django.utils import timezone

# Create your models here.
class PaypalToken(models.Model):
    scope = models.CharField(max_length=255)
    access_token = models.CharField(max_length=255)
    app_id = models.CharField(max_length=255, unique=True)
    expire_time = models.DateTimeField()

    def validate_token(self):
        if timezone.now() < self.expire_time:
            return self.access_token
        else:
            self.delete()
            return None
