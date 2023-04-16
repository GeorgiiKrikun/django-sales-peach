from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from ..models import Feedback, FeedbackFile
from django.template import loader
from django.urls import reverse
from django.utils import timezone

@login_required(login_url="authentication:login")
def feedback(request):
    context = {'problems': Feedback.topic_ids}

    html_template = loader.get_template('home/add_feedback.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="authentication:login")
def submit_feedback(request):
    if request.method == 'POST':
        print("POST " + str(request.POST))
        current_user = request.user
        feedback = Feedback()
        feedback.user = current_user
        feedback.topic_id = request.POST['topic_selection']
        feedback.feedback = request.POST['feedback_content']
        feedback.save()
        
        if request.FILES:
            for field in request.FILES:
                file = request.FILES[field]
                feedbackFile = FeedbackFile()
                feedbackFile.feedback = feedback
                file.name = str(timezone.now()) + "_" + file.name
                feedbackFile.file = file
                feedbackFile.save()
        html_template = loader.get_template('home/thank_for_your_feedback.html')
        return HttpResponse(html_template.render({}, request))
    else:
        return HttpResponseRedirect(reverse('home:feedback'))
    
