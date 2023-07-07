from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from ..models import Company, Service
from django.template import loader
from django.urls import reverse
from django.shortcuts import redirect, render
from ..forms import operation_modes, CompanyForm, ServiceForm


@login_required(login_url="authentication:login")
def edit_company(request):
    if request.method == 'POST':
        current_user = request.user
        company = Company.objects.filter(user_id=current_user.pk ).filter(name__iexact=request.POST['name']).first()
        if company is None:
            company = Company()
            company.user = current_user
            company.name = request.POST['name']
        company.about = request.POST['']
        company.save()
        return HttpResponseRedirect(reverse('speach:companies'))
    
@login_required(login_url="authentication:login")
def company(request):
    if request.method == 'POST':
        user = request.user
        if request.POST['submit'] == 'Create':
            form = CompanyForm(user=user, operation_mode=operation_modes.CREATE)
            return render(request, 'companies/company.html', {'form': form, 'operation_mode': str(operation_modes.CREATE),
                                                              'id': -1})
        elif request.POST['submit'] == 'Edit':
            id = request.POST['company_id']
            company = Company.objects.get(id=id)
            form = CompanyForm(instance = company, user=user, operation_mode=operation_modes.UPDATE)
            return render(request, 'companies/company.html', {'form': form, 'operation_mode': str(operation_modes.UPDATE),
                                                              'id': id})
        elif request.POST['submit'] == 'Save':
            if Company.objects.filter(id=request.POST['company_id']).exists():
                company = Company.objects.get(id=request.POST['company_id'])
            else:
                company = Company()

            form = CompanyForm(request.POST, user=user, instance = company)
            if form.is_valid():
                company = form.save(commit=True)
                company.save()
                return redirect(reverse('speach:companies'))
            else:
                raise ValueError("Form is not valid")
        elif request.POST['submit'] == 'Delete':
            company = Company.objects.get(id=request.POST['company_id'])
            company.delete()
            return redirect(reverse('speach:companies'))
        else:
            raise ValueError("Unknown submit value")
        
    return redirect(reverse('speach:companies'))

@login_required(login_url="authentication:login")
def add_service(request, company_id: int, service_id: int = None):
        user = request.user
        if not Company.objects.filter(id=company_id).exists():
            return HttpResponse("Company not found", status=404)
        company = Company.objects.get(id=company_id)
        service = Service.objects.get(id=service_id) if service_id is not None  and Service.objects.filter(id = service_id).exists() else None
        if (service is not None and service.company != company):
            return HttpResponse("Service not found", status=404)
        #check if company belongs to user
        if company.user_id != user.pk: #return 503
            return HttpResponse("Unauthorized", status=503)
        if request.method == 'GET':
            if service_id is None:
                form = ServiceForm(user=user, company=company, operation_mode=operation_modes.CREATE)
                return render(request, 'services/service.html', {'form': form, 'operation_mode': str(operation_modes.CREATE)})
            else:
                form = ServiceForm(instance = service, user=user, company=company, operation_mode=operation_modes.VIEW)
                return render(request, 'services/service.html', {'form': form, 'operation_mode': str(operation_modes.VIEW)})
                
        elif request.method == 'POST':
            operation_mode = operation_modes[request.POST['operation_mode']]
            if operation_mode == operation_modes.CREATE:
                form = ServiceForm(request.POST, user=user, company=company)
                if form.is_valid():
                    service = form.save(commit=True)
                    service.save()
                    return redirect(reverse('speach:companies'))
            elif operation_mode == operation_modes.UPDATE:
                form = ServiceForm(request.POST, user=user, company=company, instance = service)
                if form.is_valid():
                    service_form = form.save(commit=False)
                    service = service_form
                    service.save()
                    return redirect(reverse('speach:companies'))
            elif operation_mode == operation_modes.VIEW:
                action = request.POST['action']
                if action == 'Update':
                    form = ServiceForm(instance = service, user=user, company=company, operation_mode=operation_modes.UPDATE)
                    return render(request, 'services/service.html', {'form': form, 'operation_mode': str(operation_modes.UPDATE)})
                elif action == 'Delete':
                    service.delete()
                    return redirect(reverse('speach:companies'))
        
        return redirect(reverse('speach:companies'))

        # if request.method == 'POST':

        



        # elif request.POST['submit'] == 'Edit':
        #     id = request.POST['company_id']
        #     company = Company.objects.get(id=id)
        #     form = CompanyForm(instance = company, user=user, operation_mode=operation_modes.UPDATE)
        #     return render(request, 'companies/company.html', {'form': form, 'operation_mode': str(operation_modes.UPDATE),
        #                                                       'id': id})
        # elif request.POST['submit'] == 'Save':
        #     if Service.objects.filter(id=request.POST['service_id']).exists():
        #         service = Service.objects.get(id=request.POST['service_id'])
        #     else:
        #         service = Service()

        #     form = ServiceForm(request.POST, user=user,  instance = service)
        #     if form.is_valid():
        #         company = form.save(commit=True)
        #         company.save()
        #         return redirect(reverse('speach:companies'))
        #     else:
        #         raise ValueError("Form is not valid")
        # elif request.POST['submit'] == 'Delete':
        #     company = Company.objects.get(id=request.POST['company_id'])
        #     company.delete()
        #     return redirect(reverse('speach:companies'))
        # else:
        #     raise ValueError("Unknown submit value")
        


@login_required(login_url="authentication:login")
def companies(request):
    context = {'segment': 'companies',
               'companies': []}
               
    current_user = request.user
    companies = Company.objects.filter(user_id=current_user.pk )
    selected_id = None
    for company in companies:
        if selected_id is None:
            selected_id = company.id
        dictionary = {'company': company,
                      'services': []}
        services = Service.objects.filter(company_id=company.id)
        for service in services:
            dictionary['services'].append(service)
        context['companies'].append(dictionary)
    context['selected_id'] = selected_id

    html_template = loader.get_template('companies/companies.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="authentication:login")
def edit_company(request):
    if request.method == 'POST':
        print("POST " + str(request.POST))
    if request.POST['submit'] == 'Edit':
        company = Company.objects.get(pk=request.POST['company_id'])
        context = {'company': company,
                    'segment': 'companies'}
        html_template = loader.get_template('companies/edit_company.html')
        return HttpResponse(html_template.render(context, request))
    elif request.POST['submit'] == 'Delete':
        company = Company.objects.get(pk=request.POST['company_id'])
        company.delete()
        return HttpResponseRedirect(reverse('speach:companies', args=()))
    else:
        return HttpResponseRedirect(reverse('speach:companies', args=()))


    
@login_required(login_url="authentication:login")
def finished_edit_company(request):
    if request.method == 'POST':
        print("POST " + str(request.POST))
        company = Company.objects.get(pk=request.POST['company_id'])
        company.about = request.POST['about']
        company.name = request.POST['name']
        company.save()

    return HttpResponseRedirect(reverse('speach:companies', args=()))

@login_required(login_url="authentication:login")
def add_company(request):
    if request.method == 'POST':
        print("POST " + str(request.POST))

    context = {'segment': 'companies'}
    html_template = loader.get_template('companies/add_company.html')
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

    return HttpResponseRedirect(reverse('speach:companies', args=()))