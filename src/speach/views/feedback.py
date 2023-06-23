from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from ..models import Feedback, FeedbackFile
from django.template import loader
from django.urls import reverse
from django.utils import timezone
from django.shortcuts import render, redirect
from ..forms import FeedbackForm

@login_required(login_url="authentication:login")
def feedback(request):
    context =  {'segment': 'feedback'}
    return render(request, 'feedback/add_feedback.html', context)

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
        return render(request, 'feedback/thank_for_your_feedback.html', {'segment': 'feedback'})
    else:
        return redirect('home:feedback')
    
def form_feedback(request):
    user = request.user
    if request.method == 'GET':
        form = FeedbackForm(user=user)
        return render(request, 'feedback/add_feedback.html', {'form': form, 'segment': 'feedback'})
    elif request.method == 'POST':
        form = FeedbackForm(request.POST, user=user)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = user
            feedback.save()
        else:
            raise ValueError("Form is not valid")
        if request.FILES:
            for field in request.FILES:
                file = request.FILES[field]
                feedbackFile = FeedbackFile()
                feedbackFile.feedback = feedback
                file.name = str(timezone.now()) + "_" + file.name
                feedbackFile.file = file
                feedbackFile.save()

        return render(request, 'feedback/thank_for_your_feedback.html', {'segment': 'feedback'})
        
    
