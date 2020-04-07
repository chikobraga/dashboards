from __future__ import unicode_literals

from django.db import models
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles


# Create your models here.


class Account(models.Model):
    accountnumber = models.BigIntegerField(primary_key=True, editable=True)
    name = models.CharField(max_length=30)
    balance = models.DecimalField(max_digits=10, decimal_places=2)


class Transactions(models.Model):
    TRANS_TYPE = (
            ('D', 'Deposit'),
            ('W', 'Withdraw'),
        )
    id = models.AutoField(primary_key=True)
    transaction = models.CharField(max_length=1, choices=TRANS_TYPE)
    update_account = models.ForeignKey(Account, related_name='accounts', on_delete=models.CASCADE)
    dest_account = models.ForeignKey(Account, related_name='dest_accounts', on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=10, decimal_places=2)


class PossessionTitle(models.Model):
    COLOR = (
        ('1', 'button_preto'),
        ('2', 'button_vermelho'),
        ('3', 'button_azul'),
        ('4', 'button_amarelo'),
        ('5', 'button_verde'),
        ('6', 'button_verde1'),
        ('7', 'button_roxo'),
        ('8', 'button_laranja'),
        ('9', 'button_rosa'),
    )
    numberid = models.IntegerField(primary_key=True, editable=True)
    name_title = models.CharField(max_length=40)
    owner_title = models.ForeignKey(Account, related_name='poss_account', null=True, blank=True, on_delete=models.CASCADE)
    color = models.CharField(max_length=1, null=True, blank=True, choices=COLOR)
    value = models.DecimalField(max_digits=10, decimal_places=2)


class TitleAttr(models.Model):
    INFO_TYPE = (
        ('1', 'Casa'),
        ('2', 'Hotel'),
    )
    id = models.AutoField(primary_key=True)
    possession = models.ForeignKey(PossessionTitle, related_name='id_possession', on_delete=models.CASCADE)
    name_attr = models.CharField(max_length=30)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    type_info = models.CharField(max_length=1, choices=INFO_TYPE, blank=True, null=True)


class InfoPossession(models.Model):
    INFO_TYPE = (
        ('1', 'Casa'),
        ('2', 'Hotel'),
    )
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=30, blank=True)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    info_possession = models.ForeignKey(PossessionTitle, related_name='id_infopossession', on_delete=models.CASCADE)
    type_info = models.CharField(max_length=1, choices=INFO_TYPE, blank=True, null=True)

