# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.views.generic import RedirectView
from django.contrib import admin
from django.urls import path, include, reverse  # add this

urlpatterns = [
    path('admin/', admin.site.urls),  # Django admin route
    path("auth/", include("apps.authentication.urls")), # Auth routes - login / register
    # Leave `Home.Urls` as last the last line
    path("speach/", include("speach.urls")),
    path("finished_registration/", RedirectView.as_view(url='/speach/finished_registration', permanent=False)),
    path("", RedirectView.as_view(url='speach/', permanent=False), name='home'),
    path("stripe/", include("djstripe.urls", namespace="djstripe")),
]
