from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from ..models import Company, PastRequest, UserExtended, PaymentPlans, Payments
from django.template import loader
from django.urls import reverse
from django.utils import timezone

from django.views.generic import ListView, DetailView, UpdateView

import externals.openai as openai

@login_required(login_url="authentication:login")
def edit_company(request):
    if request.method == 'POST':
        print("POST " + str(request.POST))
        current_user = request.user
        company = Company.objects.filter(user_id=current_user.pk ).filter(name__iexact=request.POST['name']).first()
        if company is None:
            company = Company()
            company.user = current_user
            company.name = request.POST['name']
        company.about = request.POST['']
        company.save()
        return HttpResponseRedirect(reverse('home:companies'))




@login_required(login_url="authentication:login")
def companies(request):

    context = {'segment': 'companies',
               'companies': []}


    current_user = request.user
    companies = Company.objects.filter(user_id=current_user.pk )

    for company in companies:
        context['companies'].append(company)

    html_template = loader.get_template('home/companies.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="authentication:login")
def edit_company(request):
    if request.method == 'POST':
        print("POST " + str(request.POST))
    if request.POST['submit'] == 'Edit':
        company = Company.objects.get(pk=request.POST['company_id'])
        context = {'company': company,
                    'segment': 'companies'}
        html_template = loader.get_template('home/edit_company.html')
        return HttpResponse(html_template.render(context, request))
    elif request.POST['submit'] == 'Delete':
        company = Company.objects.get(pk=request.POST['company_id'])
        company.delete()
        return HttpResponseRedirect(reverse('home:companies', args=()))
    else:
        return HttpResponseRedirect(reverse('home:companies', args=()))


    
@login_required(login_url="authentication:login")
def finished_edit_company(request):
    if request.method == 'POST':
        print("POST " + str(request.POST))
        company = Company.objects.get(pk=request.POST['company_id'])
        company.about = request.POST['about']
        company.name = request.POST['name']
        company.save()

    return HttpResponseRedirect(reverse('home:companies', args=()))

@login_required(login_url="authentication:login")
def add_company(request):
    if request.method == 'POST':
        print("POST " + str(request.POST))

    context = {'segment': 'companies'}
    html_template = loader.get_template('home/add_company.html')
    return HttpResponse(html_template.render(context, request))
        

@login_required(login_url="authentication:login")
def finished_adding_company(request):
    if request.method == 'POST':
        print("POST " + str(request.POST))
        current_user = request.user
        company = Company()
        company.user = current_user
        company.about = request.POST['about']
        company.name = request.POST['name']
        company.save()

    return HttpResponseRedirect(reverse('home:companies', args=()))