# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from .models import Company, PastRequest, UserExtended, Payments, Payment, PaymentPlans, Feedback, FeedbackFile

admin.site.register(Company)
admin.site.register(Payments)
admin.site.register(PaymentPlans)
admin.site.register(UserExtended)
admin.site.register(PastRequest)
admin.site.register(Payment)
admin.site.register(Feedback)
admin.site.register(FeedbackFile)
# Register your models here.
