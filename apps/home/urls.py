# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views

app_name = "home"

urlpatterns = [

    # The home page
    path('', views.index, name='home'),
    path('profile', views.profile, name='profile'),
    path('speach', views.speach, name='speach'),
    path('get_speach', views.get_speach, name='get_speach'),
    path('speach_result', views.speach_result , name='speach_result'),

    # Matches any html file
    # re_path(r'^.*\.*', views.pages, name='pages'),

]
