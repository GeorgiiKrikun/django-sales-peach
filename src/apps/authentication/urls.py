# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, include
from .views import login_view, register_user, logout_view, reset_password, activate, reset_password_link
from django.contrib.auth.views import LogoutView

app_name = "authentication"

urlpatterns = [
    path('login/', login_view, name="login"),
    path('register/', register_user, name="register"),
    path("logout/", logout_view, name="logout"),
    path("reset_password/", reset_password, name="reset_password"),
    path("activate/<uidb64>/<token>/", activate, name="activate"),
    path('reset_password_link/<uidb64>/<token>/', reset_password_link, name='reset_password_link'),
    # path('social_login/', include('allauth.urls'),),
]
