from django import forms
from django.forms import ModelForm
from .models import *


class TransactionForm(ModelForm):
    class Meta:
        model = Transactions
        fields = ['transaction','update_account','dest_account','value']
    #transaction = forms.CharField(
    #    widget=forms.TextInput(
    #    attrs={'value': 'W',
    #           'class': 'form-control',
    #           'disabled': 'disabled',
    #           }),
    #    label='Transaction'
    #)