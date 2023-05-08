from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from djstripe.models import Product, Price, Customer
from speach.models import UserData
from django.shortcuts import render


@login_required(login_url="authentication:login")
def select_subscriptions(request):
    return render(request, 'subscriptions/select_subscriptions.html', {'products': Product.objects.all()})

@login_required(login_url="authentication:login")
def subscription_selected(request):
    if request.method == 'POST':
        price_id = request.POST.get('price_id')
        price = Price.objects.get(id=price_id)
        userData = UserData.objects.get(user=request.user.pk)
        customer = Customer.objects.get(id=userData.customer.id)
        customer.subscribe(items=[{'price': price}])

    return HttpResponseRedirect(session.url)