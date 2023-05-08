from django.urls import path, re_path
from speach.views import companies, speach

app_name = "speach"

urlpatterns = [

    # The home page
    # path('', views_general.index, name='home'),
    # path('profile', views_general.profile, name='profile'),

    # #Companies
    path('companies', companies.companies , name='companies'),
    path('edit_company', companies.edit_company , name='edit_company'),
    path('finished_editing_company', companies.finished_edit_company , name='finished_editing_company'),
    path('add_company', companies.add_company , name='add_company'),
    path('finished_adding_company', companies.finished_adding_company , name='finished_adding_company'),
    # #Payments
    # path('payments', payments.payments , name='payments'),
    # path('make_payment', payments.make_payment , name='make_payment'),
    # path('complete_payment', payments.complete_payment, name='complete_payment'),
    # #Speach
    path('', speach.speach, name='speach'),
    path('speach', speach.speach, name='speach'),
    path('get_speach', speach.get_speach, name='get_speach'),
    path('retry_speach', speach.retry_speach, name='retry_speach'),
    path('speach_result', speach.speach_result , name='speach_result'),
    path('finished_registration', speach.finished_registration , name='finished_registration'),
    # #Feedback
    # path('feedback', feedback.feedback , name='feedback'),
    # path('submit_feedback', feedback.submit_feedback , name='submit_feedback'),
    # # Test stuff
    # path('company_test_view', views_general.CompaniesListView.as_view(), name='company_test_view'),
    # path('past_req_update/<int:pk>', views_general.PastRequestUpdateView.as_view(), name='company_test_view'),
    # path('payment_details/<int:payment_id>', views_general.payment_details, name='payment_details'),
    # path('payment_success', views_general.payment_success, name='payment_success'),
    # path('payment_failure', views_general.payment_failure, name='payment_failure'),
    # # Stripe test stuff
    # path('select_subscriptions', views_general.select_subscriptions, name='select_subscriptions'),
    # path('subscription_selected', views_general.subscription_selected, name='subscription_selected'),
    # path('subscription_success', views_general.subscription_success, name='subscription_success'),
    # path('subscription_failure', views_general.subscription_failure, name='subscription_failure'),

    # # Matches any html file
    # re_path(r'^.*\.*', views_general.pages, name='pages'),

]
