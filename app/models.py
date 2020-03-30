from __future__ import unicode_literals

from django.db import models

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
    update_account = models.ForeignKey(Account, related_name='accountnumbers', on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.update_account


class PossessionTitle(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    owner_title = models.BigIntegerField(editable=True)


class TitleAttr(models.Model):
    id = models.AutoField(primary_key=True)
    possession = models.ForeignKey(PossessionTitle, ralated_name='name', on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    value = models.DecimalField(max_digits=10, decimal_places=2)

