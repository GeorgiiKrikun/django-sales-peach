from datetime import timezone
from django.contrib.auth.decorators import login_required
from speach.models import Company, PastRequest, UserData, Service
from django.urls import reverse
import externals.openai as openai
from django.shortcuts import redirect, render
from speach.forms import PastRequestForm, operation_modes
from asgiref.sync import async_to_sync, sync_to_async
from speach.views.subscribe import get_active_subscriptions
from django.contrib import messages

@login_required(login_url="authentication:login")
def speach(request):
    user = request.user
    userdata = UserData.objects.get(user=user.pk)
    if (userdata.uses_left <= 0):
        messages.error(request, 'You have no uses left. Please subscribe to get more uses.')
    if request.method == 'POST':
        if (userdata.uses_left <= 0):
            return redirect(reverse('speach:speach'))
        operation_mode = operation_modes[request.POST.get('operation_mode')]
        if operation_mode == operation_modes.CREATE:
            form = PastRequestForm(request.POST, user=user)
            if form.is_valid():
                past_request = form.save(commit=False)
                response = create_result_based_on_past_request(past_request)
                userdata.uses_left -= 1
                userdata.save()
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
            userdata.uses_left -= 1
            userdata.save()
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
    service = Service.objects.get(id=past_request.service.id)
    user_data = UserData.objects.get(user=current_user.pk)
    response = openai.get_suggestion_from_api(company.name, company.about, service.name , past_request.request, temperature)
    return response