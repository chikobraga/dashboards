from django.contrib.auth.models import User, Group
from app.models import *
from rest_framework import serializers


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['accountnumber', 'name', 'balance']


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transactions
        fields = ['id', 'transaction', 'update_account','dest_account', 'value']


class TitleAttrSerializer(serializers.ModelSerializer):
    class Meta:
        model = TitleAttr
        fields = ['id', 'possession', 'name_attr', 'value', 'type_info']


class InfoPossessionSerializer(serializers.ModelSerializer):
    class Meta:
        models = InfoPossession
        fields = ['id', 'description', 'value', 'info_possession', 'type_info']


class PossessionTitleSerializer(serializers.ModelSerializer):
    class Meta:
        models = PossessionTitle
        fields = ['numberid', 'name_title', 'owner_title', 'color', 'value']
