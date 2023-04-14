# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views_general
from apps.home.views import payments, speach, companies


app_name = "home"

urlpatterns = [

    # The home page
    path('', views_general.index, name='home'),
    path('profile', views_general.profile, name='profile'),

    #Companies
    path('companies', companies.companies , name='companies'),
    path('edit_company', companies.edit_company , name='edit_company'),
    path('finished_editing_company', companies.finished_edit_company , name='finished_editing_company'),
    path('add_company', companies.add_company , name='add_company'),
    path('finished_adding_company', companies.finished_adding_company , name='finished_adding_company'),
    #Payments
    path('payments', payments.payments , name='payments'),
    path('make_payment', payments.make_payment , name='make_payment'),
    path('complete_payment', payments.complete_payment, name='complete_payment'),
    #Speach
    path('speach', speach.speach, name='speach'),
    path('get_speach', speach.get_speach, name='get_speach'),
    path('retry_speach', speach.retry_speach, name='retry_speach'),
    path('speach_result', speach.speach_result , name='speach_result'),

    # Test stuff
    path('company_test_view', views_general.CompaniesListView.as_view(), name='company_test_view'),
    path('past_req_update/<int:pk>', views_general.PastRequestUpdateView.as_view(), name='company_test_view'),
    path('payment_details/<int:payment_id>', views_general.payment_details, name='payment_details'),
    path('payment_success', views_general.payment_success, name='payment_success'),
    path('payment_failure', views_general.payment_failure, name='payment_failure'),

    # Matches any html file
    re_path(r'^.*\.*', views_general.pages, name='pages'),

]
