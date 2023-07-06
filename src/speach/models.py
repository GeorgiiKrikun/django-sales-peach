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
    
class Service(models.Model):
    name = models.CharField(max_length=100)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    about = models.CharField(max_length=1000)
    def __str__(self):
        return self.name
    
class UserData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)
    latest_company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    email_confirmed = models.BooleanField(default=False) #NOT NEEDED TODO: REMOVE
    def __str__(self):
        return self.user.username + " " + self.email_confirmed

class PastRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    request = models.CharField(max_length=1000, default="")
    response = models.CharField(max_length=1000, blank=True, null=True, default="")
    temperature = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Feedback(models.Model):
    feedback_size = 1000
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topic_id = models.ForeignKey('FeedbackTopic', on_delete=models.CASCADE)
    feedback = models.CharField(max_length=feedback_size)

class FeedbackTopic(models.Model):
    topic = models.CharField(max_length=100)
    def __str__(self):
        return self.topic

    
class FeedbackFile(models.Model):
    feedback = models.ForeignKey(Feedback, on_delete=models.CASCADE)
    file = models.FileField(upload_to='feedback_files')