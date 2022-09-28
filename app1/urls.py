
from django.contrib import admin
from django.urls import path, include
from app1 import views


urlpatterns = [
    path('', views.getUser, name = 'home'),
    path('tweetSentiments', views.tweetSentiments, name = 'tweetSentiments'),
    path('profile', views.profile, name = 'profile'),
    path('chart', views.chart, name = 'chart'),
]