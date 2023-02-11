# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from .models import Company, PastRequest, UserExtended
from django.template import loader
from django.urls import reverse
 
import externals.openai as openai


@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def profile(request):
    context = {'segment': 'profile'}

    html_template = loader.get_template('home/profile.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
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


@login_required(login_url="/login/")
def speach(request):
   
    current_user = request.user
    companies = Company.objects.filter(user_id=current_user.pk )
    if (UserExtended.objects.filter(user=current_user.pk).exists()):
        latest_company = UserExtended.objects.get(user=current_user.pk).latest_company
    else:
        new_user_extended = UserExtended()
        new_user_extended.user = current_user
        new_user_extended.latest_company = companies.first()
        new_user_extended.save()
        latest_company = new_user_extended.latest_company

    context = {'segment': 'speach',
               'companies': companies,
               'selected_company': latest_company}

    html_template = loader.get_template('home/speach.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def get_speach(request):
    if request.method == 'POST':
        print("POST " + str(request.POST))

    company_id = request.POST['CompanySelection']
    current_user = request.user
    company = Company.objects.get(id=company_id)

    extended_user = UserExtended.objects.get(user=current_user.pk)
    extended_user.latest_company = company
    extended_user.save()

    html_template = loader.get_template('home/speach_result.html')
    
    response = openai.get_openai_response(company.name, company.about, request.POST['AboutInput'])

    context = {
               'segment': 'speach', 
               'AboutInput': request.POST['AboutInput'],
               'Result': response,
              }

    saved_request = PastRequest()
    saved_request.user = current_user
    saved_request.company = company
    saved_request.about = context["AboutInput"]
    saved_request.response = context['Result']
    saved_request.save()

    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def speach_result(request):
    if request.method == 'POST':
        print("POST " + str(request.POST['AboutInput']))


    return HttpResponseRedirect(reverse('home:speach', args=()))

@login_required(login_url="/login/")
def companies(request):

    context = {'segment': 'companies',
               'companies': []}


    current_user = request.user
    companies = Company.objects.filter(user_id=current_user.pk )

    for company in companies:
        context['companies'].append(company)

    html_template = loader.get_template('home/companies.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
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

    
@login_required(login_url="/login/")
def finished_edit_company(request):
    if request.method == 'POST':
        print("POST " + str(request.POST))
        company = Company.objects.get(pk=request.POST['company_id'])
        company.about = request.POST['about']
        company.name = request.POST['name']
        company.save()

    return HttpResponseRedirect(reverse('home:companies', args=()))

@login_required(login_url="/login/")
def add_company(request):
    if request.method == 'POST':
        print("POST " + str(request.POST))

    context = {'segment': 'companies'}
    html_template = loader.get_template('home/add_company.html')
    return HttpResponse(html_template.render(context, request))
        

@login_required(login_url="/login/")
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

@login_required(login_url="/login/")
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


