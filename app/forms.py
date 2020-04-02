from django import forms
from django.forms import ModelForm
from .models import *


class TransactionForm(ModelForm):
    class Meta:
        model = Transactions
        fields = ['transaction','update_account','dest_account','value']
        transaction = models.CharField(max_length=1, choices='W')