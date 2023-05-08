from django.contrib import admin
from .models import Company, PastRequest, UserData

admin.site.register(Company)
admin.site.register(PastRequest)
admin.site.register(UserData)
# Register your models here.
