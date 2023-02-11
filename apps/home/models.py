# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Company(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    about = models.CharField(max_length=1000)

    def __str__(self):
        return self.name

class Payments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subscription_plan_months = models.IntegerField(default=0)
    subscription_plan_requests_per_day = models.IntegerField(default=10)
    subscription_activation_date = models.DateTimeField(null=True)
    cost_of_subscription = models.FloatField(default=0.0)

class PaymentPlans(models.Model):
    name = models.CharField(max_length=100)
    background_color = models.CharField(max_length=7, default="#FFFFFF")
    cost = models.FloatField(default=0.0)
    requests_per_day = models.IntegerField(default=10)

class UserExtended(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    latest_company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)

class PastRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    response = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
