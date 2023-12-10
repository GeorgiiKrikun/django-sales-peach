from django.contrib import admin
from speach.models import Company, PastRequest, UserData, Feedback, FeedbackTopic, FeedbackFile, Service, DiscountCode

admin.site.register([Company, 
                     PastRequest, 
                     UserData, 
                     Feedback, 
                     FeedbackTopic, 
                     FeedbackFile,
                     Service])

class DiscountCodeAdmin(admin.ModelAdmin):
    list_display = ('admin_code_view', 'uses_given', 'was_sent', 'was_used', 'user_redeemed')

admin.site.register(DiscountCode, DiscountCodeAdmin)