from django.contrib.auth.decorators import login_required
from speach.models import Company, PastRequest, UserData
from django.urls import reverse
import externals.openai as openai
from django.shortcuts import redirect, render
from speach.forms import PastRequestForm, operation_modes




@login_required(login_url="authentication:login")
def speach(request):
    user = request.user
    if request.method == 'POST':
        operation_mode = operation_modes[request.POST.get('operation_mode')]
        if operation_mode == operation_modes.CREATE:
            form = PastRequestForm(request.POST, user=user)
            if form.is_valid():
                past_request = form.save(commit=False)
                response = create_result_based_on_past_request(past_request)
                past_request.response = response
                past_request.save()
            else:
                raise ValueError("Form is not valid")
            result_form = PastRequestForm(instance=past_request, user=user, operation_mode=operation_modes.VIEW)
            return render(request,'speach/speach.html', {'form':result_form, 'operation_mode': str(operation_modes.VIEW), 'id':past_request.id,
                                                         'segment': 'speach'})  
        elif operation_mode == operation_modes.VIEW:
            id = request.POST.get('id') 
            past_request = PastRequest.objects.get(id=id)
            new_temperature = min(1, past_request.temperature + 0.2)
            response = create_result_based_on_past_request(past_request, new_temperature)
            past_request.temperature = new_temperature
            past_request.response = response
            past_request.save()
            result_form = PastRequestForm(instance=past_request, user=user, operation_mode=operation_modes.VIEW)
            return render(request,'speach/speach.html', {'form':result_form, 'operation_mode': str(operation_modes.VIEW), 'id':past_request.id,
                                                         'segment': 'speach'})
    else:
        form = PastRequestForm(operation_mode = operation_modes.CREATE, user=user)
    return render(request, 'speach/speach.html', {'form': form, 'operation_mode': str(operation_modes.CREATE),
                                                  'segment': 'speach', 'id': 'none'})

def create_result_based_on_past_request(past_request: PastRequest, temperature = 0):
    company_id = past_request.company.id
    current_user = past_request.user
    company = Company.objects.get(id=company_id)
    user_data = UserData.objects.get(user=current_user.pk)
    response =  openai.get_suggestion_from_api(company.name, company.about, past_request.request, temperature)
    return response