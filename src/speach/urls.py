from django.urls import path, re_path

from speach.views import companies, speach, subscribe, registration, feedback

app_name = "speach"

urlpatterns = [

    # The home page
    # path('', views_general.index, name='home'),
    # path('profile', views_general.profile, name='profile'),

    # #Companies
    path('companies', companies.companies , name='companies'),
    # path('edit_company', companies.edit_company , name='edit_company'),
    path('company', companies.company , name='company'),
    # path('add_company', companies.add_company , name='add_company'),
    # path('finished_adding_company', companies.finished_adding_company , name='finished_adding_company'),
    #Subscriptions
    path('select_subscriptions', subscribe.select_subscriptions , name='select_subscriptions'),
    path('subscription_selected', subscribe.subscription_selected , name='subscription_selected'),
    path('payment_methods', subscribe.payment_methods , name='payment_methods'),
    path('cancel_subscription', subscribe.cancel_subscription , name='cancel_subscription'),
    path('confirm_subscription_cancel', subscribe.confirm_subscription_cancel , name='confirm_subscription_cancel'),
    path('change_subscription', subscribe.change_subscription , name='change_subscription'),
    
    # #Speach
    path('', speach.speach, name='speach'),
    path('speach', speach.speach, name='speach'),

    # #Registration
    path('finished_registration', registration.finished_registration , name='finished_registration'),
    # #Feedback
    path('feedback', feedback.form_feedback , name='feedback'),
    path('submit_feedback', feedback.submit_feedback , name='submit_feedback'),

    #Services
    path('add_service/<int:company_id>', companies.add_service , name='add_service'),
    path('add_service/<int:company_id>/<int:service_id>', companies.add_service , name='add_service'),

]
