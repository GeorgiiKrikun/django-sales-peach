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
    path('companies', views.companies , name='companies'),
    path('edit_company', views.edit_company , name='edit_company'),
    path('finished_editing_company', views.finished_edit_company , name='finished_editing_company'),
    path('add_company', views.add_company , name='add_company'),
    path('finished_adding_company', views.finished_adding_company , name='finished_adding_company'),

    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
