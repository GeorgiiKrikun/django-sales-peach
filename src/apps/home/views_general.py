# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from .models import Company, PastRequest, UserExtended, PaymentPlans, Payments
from django.template import loader
from django.urls import reverse

from django.views.generic import ListView, DetailView, UpdateView

from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from payments import get_payment_model, RedirectNeeded
from djstripe.models import Product, Plan
from djstripe import webhooks
import stripe
import os
stripe.api_key = os.environ.get("STRIPE_TEST_SECRET_KEY")



def payment_details(request, payment_id):
    payment = get_object_or_404(get_payment_model(), id=payment_id)

    try:
        form = payment.get_form(data=request.POST or None)
    except RedirectNeeded as redirect_to:
        return redirect(str(redirect_to))

    return TemplateResponse(
        request,
        'home/django-payment.html',
        {'form': form, 'payment': payment}
    )

def payment_success(request):
    html_template = loader.get_template('home/django-payments-success.html')
    return HttpResponse(html_template.render({}, request))

def payment_failure(request):
    html_template = loader.get_template('home/django-payments-failure.html')
    return HttpResponse(html_template.render({}, request))

def select_subscriptions(request):
    html_template = loader.get_template('home/select_subscriptions.html')
    return HttpResponse(html_template.render({'products': Product.objects.all()}, request))

def subscription_selected(request):
    html_template = loader.get_template('home/select_subscriptions.html')
    price_id = request.POST['price_id']
    session = stripe.checkout.Session.create(
    success_url='http://127.0.0.1:8000/speach/subscription_success',
    cancel_url='http://127.0.0.1:8000/speach/subscription_failure',
        mode='subscription',
        line_items=[{
            'price': price_id,
            # For metered billing, do not pass quantity
            'quantity': 1
        }],
    )

    return HttpResponseRedirect(session.url)

def subscription_success(request):
    html_template = loader.get_template('home/subscription_success.html')
    return HttpResponse(html_template.render({}, request))

def subscription_failure(request):
    html_template = loader.get_template('home/subscription_failure.html')
    return HttpResponse(html_template.render({}, request))

@login_required(login_url="authentication:login")
def index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="authentication:login")
def profile(request):
    context = {'segment': 'profile'}

    html_template = loader.get_template('home/profile.html')
    return HttpResponse(html_template.render(context, request))


class CompaniesListView(ListView):
    model = Company
    paginate_by = 5

    def get_queryset(self):
        return Company.objects.filter(user_id=self.request.user.pk).order_by('name')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['segment'] = 'companies'
        return context
    

class CompanyDetailedView(DetailView):
    model = Company

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['segment'] = 'companies'
        return context

class PastRequestUpdateView(UpdateView):
    model = PastRequest
    fields = ['response', 'temperature']
    template_name_suffix = '_update_form'

    
@login_required(login_url="authentication:login")
def pages(request):
    context = {}

    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:
        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))

@webhooks.handler_all
def my_handler(event, **kwargs):
    print("Triggered webhook " + event.type)