from django import forms
from django.forms import ModelForm
from .models import *


class TransactionForm(ModelForm):
    class Meta:
        model = Transactions
        transaction = forms.CharField(max_length=1)
        update_account = forms.CharField(max_length=30)
        dest_account = forms.CharField(max_length=30)
        value = forms.CharField(max_length=30)