from django.contrib import admin

# Register your models here.
from .models import SalesforceOAuthToken
# Register your models here.


class SalesforceOAuthTokenAdmin(admin.ModelAdmin):
    list_display = ("id","user", "access_token", "refresh_token", "instance_url")

admin.site.register(SalesforceOAuthToken, SalesforceOAuthTokenAdmin)
