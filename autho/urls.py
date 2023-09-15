from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("salesforce-login/", views.salesforce_login, name="salesforce-login"),
    path("auth/aaa/", views.salesforce_callback, name="salesforce-callback"),
    # path("welcome/", views.welcome, name="welcome"),
]
