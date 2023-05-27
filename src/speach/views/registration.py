
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
    messages.add_message(request, messages.INFO, 'You have successfully registered! To get access to full functionality,\
                        please confirm the e-mail address you provided.')

    return redirect("speach:speach")