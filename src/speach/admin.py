from django.contrib import admin
from speach.models import Company, PastRequest, UserData, Feedback, FeedbackTopic, FeedbackFile, Service

admin.site.register([Company, 
                     PastRequest, 
                     UserData, 
                     Feedback, 
                     FeedbackTopic, 
                     FeedbackFile,
                     Service ])