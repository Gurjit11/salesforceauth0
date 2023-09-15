# views.py
from django.shortcuts import redirect
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.http import HttpResponse
import requests
from django.template import loader
from autho import settings
from autho.models import SalesforceOAuthToken


# def home(request):
#     # template = loader.get_template("home.html")
#     return HttpResponse("go to /auth/login")


# def welcome(request):
#     return HttpResponse("Welcome to Mavlon!")


def home(request):
    return render(request, "auth/welcome.html")


def salesforce_login(request):
    salesforce_authorize_url = (
        f"https://login.salesforce.com/services/oauth2/authorize"
        f"?response_type=code"
        f"&client_id={settings.SALESFORCE_CLIENT_ID}"
        f"&redirect_uri={settings.SALESFORCE_AUTH_REDIRECT_URI}"
    )
    return redirect(salesforce_authorize_url)


def salesforce_callback(request):
    authorization_code = request.GET.get("code")

    if authorization_code:
        token_url = "https://login.salesforce.com/services/oauth2/token"
        payload = {
            "code": authorization_code,
            "grant_type": "authorization_code",
            "client_id": settings.SALESFORCE_CLIENT_ID,
            "client_secret": settings.SALESFORCE_CLIENT_SECRET,
            "redirect_uri": settings.SALESFORCE_AUTH_REDIRECT_URI,
        }

        response = requests.post(token_url, data=payload)

        if response.status_code == 200:
            data = response.json()
            access_token = data.get("access_token")
            refresh_token = data.get("refresh_token")
            instance_url = data.get("instance_url")

            user = request.user

            if user.is_authenticated:
                profile, created = SalesforceOAuthToken.objects.get_or_create(user=user)
                profile.access_token = access_token
                profile.refresh_token = refresh_token
                profile.instance_url = instance_url
                profile.save()

            return HttpResponse("welcome to Mavlon")

    return HttpResponse("OAuth process failed. Please try again.")
