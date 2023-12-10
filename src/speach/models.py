from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from djstripe.models import Customer
from decimal import Decimal
import secrets


# Create your models here.
class Company(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100)
    about = models.CharField(max_length=1000, default="")

    def __str__(self):
        return self.name
    
class Service(models.Model):
    name = models.CharField(max_length=100)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    about = models.CharField(max_length=1000, blank=True, null=True)
    def __str__(self):
        return self.name
    
class UserData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    customer = models.OneToOneField(Customer, on_delete=models.SET_NULL, null=True)
    latest_company = models.ForeignKey(Company, on_delete=models.SET_NULL, blank=True, null=True)
    email_confirmed = models.BooleanField(default=False) #NOT NEEDED TODO: REMOVE
    uses_left = models.IntegerField(default=0)
    bonus_uses = models.IntegerField(default=0)
    def __str__(self):
        return self.user.username

class PastRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True)
    request = models.CharField(max_length=1000, default="")
    response = models.CharField(max_length=1000, blank=True, null=True, default="")
    temperature = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class DiscountCode(models.Model):
    code = models.CharField(max_length=16, blank=True)
    uses_given = models.IntegerField(default=5)
    was_used = models.BooleanField(default=False)
    was_sent = models.BooleanField(default=False)
    user_redeemed = models.ForeignKey(User, on_delete=models.SET_NULL, blank = True, null = True)

    def save(self, *args, **kwargs):
        if not self.code:  # only set code if it's not already set
            self.code = DiscountCode.generate_random_code()
        super().save(*args, **kwargs)

    def code_to_display_code(code: str) -> str:
        return f"{code[:4]}-{code[4:8]}-{code[8:12]}-{code[12:16]}"

    def display_code_to_code(display_code: str) -> str:
        return display_code.replace("-", "").replace(" ", "")
    
    def admin_code_view(self):
        return DiscountCode.code_to_display_code(self.code)

    def generate_random_code()-> str:
        return secrets.token_hex(8)

    def __str__(self):
        if self.was_used:
            return f"(used) discount for {self.uses_given}"
        if self.was_sent:
            return f"(sent) discount for {self.uses_given}"
        return f"discount for {self.uses_given}"

class Feedback(models.Model):
    feedback_size = 1000
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topic_id = models.ForeignKey('FeedbackTopic', on_delete=models.SET_NULL, null=True)
    feedback = models.CharField(max_length=feedback_size)

class FeedbackTopic(models.Model):
    topic = models.CharField(max_length=100)
    def __str__(self):
        return self.topic

    
class FeedbackFile(models.Model):
    feedback = models.ForeignKey(Feedback, on_delete=models.CASCADE)
    file = models.FileField(upload_to='feedback_files')