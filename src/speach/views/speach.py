from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from ..models import Company, PastRequest, UserData
from django.template import loader
from django.urls import reverse
from django.utils import timezone
import externals.openai as openai
from django.shortcuts import redirect
from djstripe.models import Customer

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

@login_required(login_url="authentication:login")
def speach(request):
   
    current_user = request.user
    companies = Company.objects.filter(user_id=current_user.pk )

    user_extended = UserData.objects.get(user=current_user.pk)
    # last_used = user_extended.last_activity

    #check if last used was yesterday, if so reset requests today
    # if (timezone.now() - last_used).days > 0 or last_used.day < timezone.now().day :
    #     user_extended.requests_today = 0
    #     user_extended.save()

    # requests_today = user_extended.requests_today    
    # max_requests_per_day = UserData.objects.get(user=current_user.pk).subscription_plan.requests_per_day
    # if (requests_today >= max_requests_per_day):
    #     html_template = loader.get_template('home/payments.html')
    #     plans = PaymentPlans.objects.all().filter(available_to_select=True)
    #     context = {'segment': 'payments',
    #                'plans': plans}
    #     return HttpResponse(html_template.render(context, request))


    context = {'segment': 'speach',
               'companies': companies,
               'selected_company': latest_company}

    html_template = loader.get_template('speach/speach.html')
    return HttpResponse(html_template.render(context, request))

# @login_required(login_url="authentication:login")
# def finished_registration(request):


@login_required(login_url="authentication:login")
def get_speach(request):
    if request.method == 'POST':
        print("POST " + str(request.POST))

    company_id = request.POST['CompanySelection']
    current_user = request.user
    company = Company.objects.get(id=company_id)

    temperature = 0

    extended_user = UserData.objects.get(user=current_user.pk)
    extended_user.latest_company = company
    extended_user.requests_today = extended_user.requests_today + 1
    extended_user.last_activity = timezone.now()
    extended_user.save()

    html_template = loader.get_template('speach/speach_result.html')
    
    response = openai.get_openai_response(company.name, company.about, request.POST['AboutInput'], temperature)

    saved_request = PastRequest()
    saved_request.user = current_user
    saved_request.company = company
    saved_request.about = request.POST["AboutInput"]
    saved_request.response = response
    saved_request.temperature = temperature
    saved_request.save()

    context = {
               'segment': 'speach', 
               'PastRequest': saved_request,
               'About': request.POST['AboutInput']
              }

    return HttpResponse(html_template.render(context, request))



@login_required(login_url="authentication:login")
def retry_speach(request):
    if request.method == 'POST':
        print("POST " + str(request.POST))  
    #Get past request object from id 
    past_requst = PastRequest.objects.get( id=request.POST['past_request_id'] )
        

    current_user = request.user
    company = past_requst.company

    temperature = min(past_requst.temperature + 0.5, 1.0)

    extended_user = UserData.objects.get(user=current_user.pk)
    extended_user.latest_company = company
    extended_user.requests_today = extended_user.requests_today + 1
    extended_user.last_activity = timezone.now()
    extended_user.save()

    html_template = loader.get_template('speach/speach_result.html')
    
    response = openai.get_openai_response(company.name, company.about, request.POST['past_about'], temperature)

    saved_request = PastRequest()
    saved_request.user = current_user
    saved_request.company = company
    saved_request.response = response
    saved_request.temperature = temperature
    saved_request.save()

    context = {
               'segment': 'speach', 
               'PastRequest': saved_request,
               'About': request.POST['past_about']
              }

    return HttpResponse(html_template.render(context, request))

@login_required(login_url="authentication:login")
def speach_result(request):
    if request.method == 'POST':
        print("POST " + str(request.POST['AboutInput']))
    return HttpResponseRedirect(reverse('speach:speach', args=()))