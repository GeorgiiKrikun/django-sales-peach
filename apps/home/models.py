# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.
# mypaymentapp/models.py
from decimal import Decimal

from payments import PurchasedItem
from payments.models import BasePayment

class Payment(BasePayment):

    def get_failure_url(self) -> str:
        # Return a URL where users are redirected after
        # they fail to complete a payment:
        # return f"http://example.com/payments/{self.pk}/failure"
        return "http://127.0.0.1:8000/speach/payment_failure/"

    def get_success_url(self) -> str:
        # Return a URL where users are redirected after
        # they successfully complete a payment:
        # return f"http://example.com/payments/{self.pk}/success"
        return "http://127.0.0.1:8000/speach/payment_success/"

    def get_purchased_items(self): #-> Iterable[PurchasedItem]:
        # Return items that will be included in this payment.
        yield PurchasedItem(
            name='The Hound of the Baskervilles',
            sku='BSKV',
            quantity=9,
            price=Decimal(10),
            currency='USD',
        )

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
    available_to_select = models.BooleanField(default=False)


class UserExtended(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subscription_plan = models.ForeignKey(PaymentPlans, on_delete=models.SET_NULL, null=True)
    last_activity = models.DateTimeField(default=timezone.now(), editable=True)
    requests_today = models.IntegerField(default=0)

    latest_company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)

class PastRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    response = models.CharField(max_length=1000)
    temperature = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
