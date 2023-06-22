from typing import Any, Dict, Mapping, Optional, Type, Union
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from .models import PastRequest,Company, Feedback, FeedbackTopic
from django.forms import *
from enum import Enum

class operation_modes(Enum):
    VIEW = 0
    CREATE = 1
    UPDATE = 2
    def __str__(self) -> str:
        return self.name

class CompanyForm(ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'about']

    def __init__(self, *args, **kwargs) -> None:
        operation_mode = kwargs.pop("operation_mode", operation_modes.VIEW)
        assert operation_mode in operation_modes, f"Invalid operation mode {operation_mode}"
        self.user = kwargs.pop("user", None)
        assert self.user is not None, "User must be provided"

        super().__init__(*args, **kwargs)
        self.fields['name'].widget = TextInput(
            attrs={
                "placeholder": "Write here something about the company you are writing to",
                "name":"name",
                "class":"form-control",
                "id":"company_name",
            })
        self.fields['about'].widget = Textarea(
            attrs={
                "name":"response",
                "class":"form-control",
                "id":"respose_text",
                "rows":"5",
            }
        )

        if operation_mode == operation_modes.VIEW:
            for field in [f for f in self.fields if f is not None]:
                self.fields[field].widget.attrs['disabled'] = True


    
    def save(self, commit=True):
        req = super().save(commit=False)
        req.user = self.user
        if commit:
            req.save()
        return req
    
class FeedbackForm(ModelForm):
    class Meta:
        model = Feedback
        fields = ['feedback', 'topic_id']

    def __init__(self, *args, **kwargs) -> None:
        self.user = kwargs.pop("user", None)
        assert self.user is not None, "User must be provided"
        super().__init__(*args, **kwargs)

        self.fields['feedback'].widget = Textarea(
            attrs={
                "name":"feedback",
                "class":"form-control",
                "id":"feedback_text",
                "rows":"5",
            }
        )
        self.fields['topic_id'].widget = Select(
            attrs={
                "class": "form-control",
                "id": "topic_id",
            },
        )
        self.fields['topic_id'].queryset = FeedbackTopic.objects.all()

    def save(self, commit=True):
        req = super().save(commit=False)
        req.user = self.user
        if commit:
            req.save()
        return req

class PastRequestForm(ModelForm):
    
    class Meta:
        model = PastRequest
        fields = ['company', 'request', 'response']
    

    def __init__(self, *args, **kwargs) -> None:
        operation_mode = kwargs.pop("operation_mode", operation_modes.VIEW)
        assert operation_mode in operation_modes, f"Invalid operation mode {operation_mode}"
        self.user = kwargs.pop("user", None)
        assert self.user is not None, "User must be provided"

        super().__init__(*args, **kwargs)



        self.fields['company'].widget = Select(
            attrs={
                "class": "form-control",
                "id": "company_name",
            },
        )

        self.fields['request'].widget = Textarea(
            attrs={
                "placeholder": "Write here something about the company you are writing to",
                "name":"AboutInput",
                "class":"form-control",
                "id":"company_description",
                "rows":"3",
            }
        )

        self.fields['response'].widget = Textarea(
            attrs={
                "name":"response",
                "class":"form-control",
                "id":"respose_text",
                "rows":"5",
            }
        )

        if operation_mode == operation_modes.VIEW:
            for field in [f for f in self.fields if f is not None]:
                self.fields[field].widget.attrs['disabled'] = True

        self.fields['company'].queryset = Company.objects.filter(user_id=self.user.pk)
    
        

    class Meta:
        model = PastRequest
        fields = ['company', 'request', 'response']

    def save(self, commit=True):
        req = super().save(commit=False)
        req.user = self.user
        if commit:
            req.save()
        return req