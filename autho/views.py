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
    # Redirect the user to Salesforce for OAuth authentication
    # Build the Salesforce OAuth authorization URL
    salesforce_authorize_url = (
        f"https://login.salesforce.com/services/oauth2/authorize"
        f"?response_type=code"
        f"&client_id={settings.SALESFORCE_CLIENT_ID}"
        f"&redirect_uri={settings.SALESFORCE_AUTH_REDIRECT_URI}"
    )
    return redirect(salesforce_authorize_url)


def salesforce_callback(request):
    # Handle the callback from Salesforce after successful authentication
    authorization_code = request.GET.get("code")

    if authorization_code:
        # Construct the request to get the access token
        token_url = "https://login.salesforce.com/services/oauth2/token"
        payload = {
            "code": authorization_code,
            "grant_type": "authorization_code",
            "client_id": settings.SALESFORCE_CLIENT_ID,
            "client_secret": settings.SALESFORCE_CLIENT_SECRET,
            "redirect_uri": settings.SALESFORCE_AUTH_REDIRECT_URI,
        }

        # Make a POST request to Salesforce to exchange the authorization code for an access token
        response = requests.post(token_url, data=payload)

        if response.status_code == 200:
            # Successfully obtained access token
            data = response.json()
            access_token = data.get("access_token")
            refresh_token = data.get("refresh_token")
            instance_url = data.get("instance_url")

            # Get the authenticated user
            user = request.user

            # Ensure the user is authenticated
            if user.is_authenticated:
                # Create or retrieve SalesforceOAuthToken for the user
                profile, created = SalesforceOAuthToken.objects.get_or_create(user=user)
                profile.access_token = access_token
                profile.refresh_token = refresh_token
                profile.instance_url = instance_url
                profile.save()

            # Redirect to a success page or perform further actions
            return HttpResponse("welcome to Mavlon")

    # Handle the case where the OAuth process failed
    return HttpResponse("OAuth process failed. Please try again.")
