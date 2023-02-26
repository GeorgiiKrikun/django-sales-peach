from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from ..models import UserExtended, PaymentPlans
from django.template import loader
from django.urls import reverse

@login_required(login_url="authentication:login")
def payments(request):
    plans = PaymentPlans.objects.all().filter(available_to_select=True)
    context = {'segment': 'payments',
               'plans': plans}
    html_template = loader.get_template('home/payments.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="authentication:login")
def make_payment(request):
    print(request.GET)
    plan_id = request.GET.get('id')
    selected_plan = PaymentPlans.objects.get(pk=plan_id)
    print("SELECTED PLAN = " + str(selected_plan.id) + " " + selected_plan.name + " " + str(selected_plan.cost))
    context = {'segment': 'payments',
               'plan': selected_plan}
    html_template = loader.get_template('home/payment_form.html')
    return HttpResponse(html_template.render(context, request))
    # return HttpResponseRedirect(reverse('home:payments', args=()))

@login_required(login_url="authentication:login")
def complete_payment(request):
    context = {'segment': 'payments'}
    plan = PaymentPlans.objects.get(pk = request.POST['plan'])
    user = request.user
    user_extended = UserExtended.objects.filter(user=user).first()
    user_extended.subscription_plan = plan
    user_extended.requests_today = 0
    user_extended.save()
    return HttpResponseRedirect(reverse('home:payments', args=()))