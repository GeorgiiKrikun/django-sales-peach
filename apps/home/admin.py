# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from .models import Company, PastRequest

admin.site.register(Company)
admin.site.register(PastRequest)

# Register your models here.
