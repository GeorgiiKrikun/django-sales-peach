
from django.shortcuts import  redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ..models import UserData, Customer

@login_required(login_url="authentication:login")
def finished_registration(request):
    if (UserData.objects.filter(user=request.user.pk).exists()):
        return redirect("speach:speach")
    current_user = request.user
    userData = UserData()
    userData.user = current_user
    new_customer = Customer.create(current_user)
    userData.customer = new_customer
    userData.save()

    return redirect("speach:speach")