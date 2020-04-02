from django import forms
from django.forms import ModelForm
from .models import *


class TransactionForm(ModelForm):
    class Meta:
        model = Transactions
        fields = ['transaction','update_account','dest_account','value']

