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
from django.utils import timezone

from django.views.generic import ListView, DetailView, UpdateView

import externals.openai as openai


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


