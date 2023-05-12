from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from djstripe.models import Product, Price, Customer, PaymentMethod
from speach.models import UserData
from django.shortcuts import render, redirect
import stripe
import os
import logging
from djstripe import webhooks

logger=logging.getLogger(__name__)

stripe.api_key = os.environ.get("STRIPE_TEST_SECRET_KEY")

@login_required(login_url="authentication:login")
def select_subscriptions(request):
    return render(request, 'subscriptions/select_subscriptions.html', {'products': Product.objects.all()})

def payment_methods(request):
    if request.method == 'GET':
        userData = UserData.objects.get(user=request.user.pk)
        session = stripe.checkout.Session.create(
            success_url='http://127.0.0.1:8000/speach/select_subscriptions',
            cancel_url='http://127.0.0.1:8000/speach/',
            mode='setup',
            customer=userData.customer.id,
            currency='eur',
            payment_method_types=['card','sofort','sepa_debit'],
        )
        if session is not None:
            return HttpResponseRedirect(session.url)
    return HttpResponseRedirect(reverse('speach:speach', args=()))



@login_required(login_url="authentication:login")
def subscription_selected(request):
    if request.method == 'POST':
        price_id = request.POST.get('price_id')
        price = Price.objects.get(id=price_id)
        userData = UserData.objects.get(user=request.user.pk)
        customer = Customer.objects.get(id=userData.customer.id)

        payment_methods_exists = PaymentMethod.objects.filter(customer=customer.id).exists()
        if payment_methods_exists:
            customer.subscribe(items=[{'price': price}])
        else:
            return redirect(reverse('speach:payment_methods'))

    return redirect(reverse('speach:select_subscriptions'))

@webhooks.handler('payment_method.attached')
def payment_method_attached(event):
    try:
        print(event)
        customer = Customer.objects.get(id=event.customer.id)
        payment_method = PaymentMethod.objects.get(id=event.data['object']['id'])
        stripe.Customer.modify(
            customer.id,
            invoice_settings={'default_payment_method': payment_method.id}
        )
        
    except Customer.DoesNotExist or PaymentMethod.DoesNotExist:
        logger.error(f"Customer {event.customer.id} or PaymentMethod {event.data.object.id}does not exist")

    
