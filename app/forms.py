from django import forms
from django.forms import ModelForm
from .models import *


class TransactionForm(ModelForm):
    class Meta:
        model = Transactions
        transaction = models.CharField(max_length=1)