from django import forms
from django.utils import timezone

class JobAddForm(forms.Form):
    title = forms.CharField(max_length=20, min_length=2)
    company = forms.CharField(max_length=20, min_length=2)
    status = forms.IntegerField()
    content = forms.CharField()
    job_link = forms.URLField()
    company_link = forms.URLField(required=False)
    applied_at = forms.DateField(required=False, initial=timezone.now,
                                     widget=forms.DateInput(attrs={'type': 'date'}))

class JobEditForm(forms.Form):
    status = forms.IntegerField()
    applied_at = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))

