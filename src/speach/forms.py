from typing import Any, Dict, Mapping, Optional, Type, Union
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from speach.models import PastRequest, Company, Feedback, FeedbackTopic, Service
from django.forms import *
from enum import Enum
import logging

class MySelectWidget(Widget):
    def __init__(self, attrs=... ) -> None:
        super().__init__(attrs)
        self._context = []
        self.template_name = "widgets/SelectWidget.html"
    
    def get_context(self, name: str, value: Any, attrs) -> Dict[str, Any]:
        context= super().get_context(name, value, attrs)
        context['opts'] = self._context
        return context
    
    def add_value(self, value: str, label:str, additional:str = "") -> None:
        self._context.append({"value":value, "label":label, 
                              "additional":additional})   

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
    
class ServiceForm(ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'about']

    def __init__(self, *args, **kwargs) -> None:
        operation_mode = kwargs.pop("operation_mode", operation_modes.VIEW)
        assert operation_mode in operation_modes, f"Invalid operation mode {operation_mode}"
        self.user = kwargs.pop("user", None)
        assert self.user is not None, "User must be provided"
        self.company = kwargs.pop("company", None)
        assert self.company is not None, "Company must be provided"

        super().__init__(*args, **kwargs)
        self.fields['name'].widget = TextInput(
            attrs={
                "placeholder": f"Name of the service or product company {self.company.name} provides",
                "name":"name",
                "class":"form-control",
                "id":"company_name",
            })
        self.fields['about'].widget = Textarea(
            attrs={
                "name":f"Description of the service or product company {self.company.name} provides",
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
        req.company = self.company
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
        fields = ['company', 'service', 'request', 'response']
        # fields = "__all__"
    
    def __init__(self, *args, **kwargs) -> None:
        operation_mode = kwargs.pop("operation_mode", operation_modes.VIEW)
        assert operation_mode in operation_modes, f"Invalid operation mode {operation_mode}"
        self.user = kwargs.pop("user", None)
        assert self.user is not None, "User must be provided"

        super().__init__(*args, **kwargs)

        logging.warning(self.fields)

        self.fields['company'].widget = Select(
            attrs={
                "class": "form-control",
                "id": "company_name",
            }
        )

        self.fields['service'].widget = MySelectWidget(
            attrs={
                "class": "form-control",
                "id": "service_name",
            },
        )
        select_widget = self.fields['service'].widget

        companies = Company.objects.filter(user_id=self.user.pk).order_by('pk','name')
        self.fields['company'].widget.choices = [(c.pk, c.name) for c in companies]
        for c in companies:
            services = Service.objects.filter(company_id=c.pk)
            for s in services:
                select_widget.add_value(s.pk, s.name, s.company.pk)

        
        # for s in services:
        #     self.fields['service'].widget.create_option(s.name, s.pk, s.company.name, False, s.pk)

        self.fields['request'].widget = Textarea(
            attrs={
                "placeholder": "Write here something about the company you are writing to",
                "name":"AboutInput",
                "class":"form-control",
                "id":"company_description",
                "rows":"5",
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
            for field in self.fields:
                f = self.fields[field]
                if f is None or f.widget is None:
                    continue
                f.widget.attrs['disabled'] = True
                
            # for field in [f for f in self.fields if f is not None and f.widget is not None]:
            #     self.fields[field].widget.attrs['disabled'] = True
        if operation_mode == operation_modes.CREATE:
            self.fields['response'].widget.attrs['hidden'] = True
            self.fields['response'].label = ""
    
        

    def save(self, commit=True):
        req = super().save(commit=False)
        req.user = self.user
        if commit:
            req.save()
        return req