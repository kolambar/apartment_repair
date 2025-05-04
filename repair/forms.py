from django import forms
from django.forms import DateInput

from .models import Flat, Owner, Operation


class FlatForm(forms.ModelForm):
    class Meta:
        model = Flat
        fields = '__all__'
        widgets = {
            'intOwnerId': forms.Select(attrs={'class': 'form-control'}),
            'txtFlatAddress': forms.TextInput(attrs={'class': 'form-control'}),
            'fltArea': forms.NumberInput(attrs={'class': 'form-control'}),
            'intCount': forms.NumberInput(attrs={'class': 'form-control'}),
            'intStorey': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class OperationForm(forms.ModelForm):
    class Meta:
        model = Operation
        fields = ['datOperationDate', 'intOperationTypeId', 'intWorkerId', 'txtOperationDescription']
        widgets = {
            'datOperationDate': DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'intOperationTypeId': forms.Select(attrs={'class': 'form-control'}),
            'intWorkerId': forms.Select(attrs={'class': 'form-control'}),
            'txtOperationDescription': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
