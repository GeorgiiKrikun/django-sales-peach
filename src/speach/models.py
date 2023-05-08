from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from djstripe.models import Customer
from decimal import Decimal



# Create your models here.
class Company(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    about = models.CharField(max_length=1000)

    def __str__(self):
        return self.name
    
class UserData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)
    latest_company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)

class PastRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    response = models.CharField(max_length=1000)
    temperature = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)