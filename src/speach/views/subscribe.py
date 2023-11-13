from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from djstripe.models import Product, Price, Customer, PaymentMethod, Subscription, SubscriptionItem
from speach.models import UserData
from django.shortcuts import render, redirect
import stripe
import os
import logging
from djstripe import webhooks
import time
from django.contrib import messages

logger=logging.getLogger(__name__)

stripe.api_key = os.environ.get("STRIPE_TEST_SECRET_KEY")

def get_active_subscriptions(user):
    userdata= UserData.objects.get(user=user)
    customer = Customer.objects.get(id=userdata.customer.id)
    subscriptions = Subscription.objects.filter(customer=customer.id).filter(status='active')
    return subscriptions

@login_required(login_url="authentication:login")
def select_subscriptions(request):
    active_subscriptions = get_active_subscriptions(request.user.pk)
    userdata = UserData.objects.get(user=request.user.pk)

    has_subscription, subscription = False, None
    if (active_subscriptions.exists()):
        has_subscription=True
        subscription = active_subscriptions.first()
    if active_subscriptions.count() > 1:
        raise Exception("User has more than one active subscription")
    
    context = {'products': []}
    for product in Product.objects.filter(active=True):
        context['products'].append({'product': product, 'prices': Price.objects.filter(product=product ).filter(active=True)})

    context['segment'] = 'payments'
    context['has_subscription'] = has_subscription
    if has_subscription:
        context['active_price'] = SubscriptionItem.objects.get(subscription=subscription.id).price
        context['active_product'] = context['active_price'].product
    
    context['remaining_uses'] = userdata.uses_left
    return render(request, 'subscriptions/select_subscriptions.html', context)

@login_required(login_url="authentication:login")
def confirm_subscription_cancel(request):
    return render(request, 'subscriptions/confirm_subscription_cancel.html', {'segment': 'payments'})


@login_required(login_url="authentication:login")
def payment_methods(request):
    if request.method == 'GET':
        domain = request.get_host()
        userData = UserData.objects.get(user=request.user.pk)
        session = stripe.checkout.Session.create(
            success_url=f'http://{domain}/speach/select_subscriptions',
            cancel_url=f'http://{domain}/speach/',
            mode='setup',
            customer=userData.customer.id,
            currency='eur',
            payment_method_types=['card','sofort','sepa_debit'],
        )
        if session is not None:
            return HttpResponseRedirect(session.url)
    
    return HttpResponseRedirect(reverse('speach:speach', args=()))





@login_required(login_url="authentication:login")
def active_subscriptions(request):
    subscriptions = get_active_subscriptions(request.user.pk)
    plans = []
    for subscription in subscriptions:
        plans.append(subscription.plan)

    return render(request, 'subscriptions/active_subscriptions.html', context={'plans': plans})

@login_required(login_url="authentication:login")
def cancel_subscription(request):
    userdata = UserData.objects.get(user=request.user.pk)
    userdata.bonus_uses += userdata.uses_left
    userdata.uses_left = 0
    userdata.save()

    subscriptions = get_active_subscriptions(request.user.pk)
    for subscription in subscriptions:
        subscription.cancel()
    return redirect(reverse('speach:select_subscriptions'), context = {'segment': 'payments'})

@login_required(login_url="authentication:login")
def subscription_selected(request):
    if request.method == 'POST':
        price_id = request.POST.get('price_id')
        price = Price.objects.get(id=price_id)
        userData = UserData.objects.get(user=request.user.pk)
        customer = Customer.objects.get(id=userData.customer.id)

        payment_methods_exists = PaymentMethod.objects.filter(customer=customer.id).exists()
        if payment_methods_exists:
            try:
                customer.subscribe(items=[{'price': price}])
            except:
                messages.error(request, f"Something went wrong. Try to reattach payment method.")
                return redirect(reverse('speach:payment_methods'))

        else:
            return redirect(reverse('speach:payment_methods'))
    time.sleep(2)
    return redirect(reverse('speach:select_subscriptions'), context = {'segment': 'payments'})

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

@webhooks.handler('invoice.paid')
def payment_succeeded(event):
    customer = event.customer
    userData = UserData.objects.get(customer=customer)
    subscription_id = event.data['object']['subscription']
    subscription = Subscription.objects.get(id=subscription_id)
    new_uses = subscription.plan.product.metadata["use_pm"]
    userData.uses_left = int(new_uses)
    if userData.bonus_uses > 0:
        userData.uses_left += userData.bonus_uses
        userData.bonus_uses = 0
    userData.save()

@webhooks.handler('customer.subscription.updated')
def subscription_updated(event):
    print(event)

@webhooks.handler('customer.subscription.deleted')
def subscription_deleted(event):
    customer = event.customer
    userData = UserData.objects.get(customer=customer)
    userData.uses_left = 0
    userData.save()
    
