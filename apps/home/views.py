# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from .models import Company, PastRequest
from django.template import loader
from django.urls import reverse
import openai
import os

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
def speach(request):
    context = {'segment': 'speach',
               'company_options': ["amazon", "celantur"]}

    current_user = request.user

    html_template = loader.get_template('home/speach.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def get_speach(request):
    if request.method == 'POST':
        print("POST " + str(request.POST))

    company = request.POST.get('CompanySelection')
    print(company)
    current_user = request.user
    company = Company.objects.filter(user_id=current_user.pk ).filter(name__iexact=company).first()


    # print(current_user.username + " " + company.name)



    html_template = loader.get_template('home/speach_result.html')
    my_description = "I work in company named " + str(company.name) + "." + " We do the following " + str(company.about) + "."
    my_description += "I want to sell it to the company" 
    my_description += ", that has following about description on their webpage info: " + str(request.POST['AboutInput'])
    my_description += ". Write me a letter to the CEO of the company that will convince him to buy my product. Format it properly."
    openai.organization = "org-Mos6UT6EjhlhAQjS4A2Gev4j"
    openai.api_key = os.getenv("OPENAI_API_KEY", default=None)
    print(my_description)
    response = openai.Completion.create(
    engine="text-davinci-002",
    prompt=my_description,
    temperature=0.5,
    max_tokens=512,
    top_p=1.0,
    frequency_penalty=0.0,
    presence_penalty=0.0)



    context = {'segment': 'speach', 
               'AboutInput': request.POST['AboutInput'],
               'Result': response['choices'][0]['text'],
              }

    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def speach_result(request):
    if request.method == 'POST':
        print("POST " + str(request.POST['AboutInput']))


    return HttpResponseRedirect(reverse('home:speach', args=()))

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


