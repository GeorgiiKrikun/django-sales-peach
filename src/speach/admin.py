from django.contrib import admin
from .models import Company, PastRequest, UserData, Feedback, FeedbackTopic, FeedbackFile, Service

admin.site.register([Company, PastRequest, UserData, Feedback, FeedbackTopic, FeedbackFile,Service ])
# admin.site.register(PastRequest)
# admin.site.register(UserData)
# admin.site.register(Feedback)
# admin.site.register(FeedbackTopic)
# admin.site.register(FeedbackFile)
# Register your models here.
