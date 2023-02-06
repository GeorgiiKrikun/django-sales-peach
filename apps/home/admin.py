# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from .models import Company, PastRequest, UserExtended, Payments

admin.site.register(Company)
admin.site.register(Payments)
admin.site.register(UserExtended)
admin.site.register(PastRequest)

# Register your models here.
