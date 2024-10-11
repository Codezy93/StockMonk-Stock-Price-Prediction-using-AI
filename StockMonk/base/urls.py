from django.urls import path
from . import views

from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('', views.home, name="HomePage"),
    path('about', views.about, name="AboutPage"),
    path('contact', views.contact, name="ContactPage"),
    path('trial', views.trial, name="TrialPage"),
    path('demo', views.demo, name="DemoPage"),
]