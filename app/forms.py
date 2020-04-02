from django import forms
from django.forms import ModelForm
from .models import *


class TransactionForm(ModelForm):
    class Meta:
        model = Transactions
        fields = ['Transaction','update_account','dest_account','value']
    transaction = forms.CharField(
        widget=forms.TextInput(
        attrs={ 'value': 'W',
               'class': 'form-control',
               'disabled': 'disabled',
                'type': 'checkbox',
               })
    )
    update_account = forms.CharField(max_length=30)
    dest_account = forms.CharField(max_length=30)
    value = forms.CharField(max_length=30)