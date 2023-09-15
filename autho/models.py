
# Create your models here.
from django.db import models

# Create your models here.
class SalesforceOAuthToken(models.Model):
    user = models.OneToOneField("auth.User",on_delete=models.CASCADE)
    access_token = models.CharField(max_length=1000)
    refresh_token = models.CharField(max_length=1000)
    instance_url = models.CharField(max_length=1000)