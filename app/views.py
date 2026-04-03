from decimal import Decimal

from django.contrib.auth import authenticate, login as auth_login
from django.db import transaction
from django.db.models import Sum
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.template.exceptions import TemplateDoesNotExist
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from app.models import Account, InfoPossession, PossessionTitle, TitleAttr, Transactions
from app.serializers import (
    AccountSerializer,
    InfoPossessionSerializer,
    PossessionTitleSerializer,
    TitleAttrSerializer,
    TransactionSerializer,
)


def index(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            numberaccount = Account.objects.get(user=user)
            account = f'account/{numberaccount.accountnumber}/'
            auth_login(request, user)
            return HttpResponseRedirect(account)
        message = 'Invalid login or password, please try again'
    else:
        message = ''

    return render(request, 'app/login.html', {'message': message})


def gentella_html(request):
    context = {}

    # The template to be loaded as per gentelella.
    # All resource paths for gentelella end in .html.
    load_template = request.path.split('/')[-1]

    try:
        return render(request, f'app/{load_template}', context)
    except TemplateDoesNotExist as exc:
        raise Http404 from exc


def Account_html(request, number):
    try:
        if request.method == 'POST':
            name = request.POST.get('maketransfer')
            account = request.POST.get('account')
            op_name = request.POST.get('op_name')
            value_rec = request.POST.get('value')
            ti_name = request.POST.get('ti_name')
            op_name_ti = request.POST.get('op_name_ti')
            if name == 'transfer':
                make_update(account, op_name, value_rec)
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', f'/account/{number}/'))
            if name == 'titulo':
                numberac = Account.objects.get(pk=op_name_ti)
                titulo = PossessionTitle.objects.get(pk=ti_name)
                titulo.owner_title = numberac
                titulo.save()
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', f'/account/{number}/'))

        account = Account.objects.get(pk=number)
        if PossessionTitle.objects.filter(owner_title=account).exists():
            totalp = PossessionTitle.objects.filter(owner_title=account).aggregate(patrimony=Sum('value'))
            finalsum = account.balance + totalp['patrimony']
        else:
            finalsum = account.balance
        others_c = Account.objects.all()
        p_attr = TitleAttr.objects.all()
        p_info = InfoPossession.objects.all()
        p_title = PossessionTitle.objects.filter(owner_title=account)
        transacao = Transactions.objects.filter(update_account=account).order_by('id')
        context = {
            'number': account,
            'transacao': transacao,
            'others_c': others_c,
            'p_title': p_title,
            'p_attr': p_attr,
            'p_info': p_info,
            'patrimony': finalsum,
        }
    except Account.DoesNotExist as exc:
        raise Http404 from exc
    return render(request, 'app/plain_page.html', context)


class AccountList(APIView):
    def get(self, request, format=None):
        account = Account.objects.all()
        serializer = AccountSerializer(account, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AccountDetail(APIView):
    def get_object(self, pk):
        try:
            return Account.objects.get(pk=pk)
        except Account.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        account = self.get_object(pk)
        serializer = AccountSerializer(account)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        account = self.get_object(pk)
        serializer = AccountSerializer(account, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        account = self.get_object(pk)
        account.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TransactionList(APIView):
    def get(self, request, format=None):
        transaction_list = Transactions.objects.all()
        serializer = TransactionSerializer(transaction_list, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            created_transaction = make_update(
                serializer.validated_data['update_account'].pk,
                serializer.validated_data['dest_account'].pk,
                serializer.validated_data['value'],
            )
            return Response(TransactionSerializer(created_transaction).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TransactionDetail(APIView):
    def get_object(self, pk):
        try:
            return Transactions.objects.get(pk=pk)
        except Transactions.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        transaction_item = self.get_object(pk)
        serializer = TransactionSerializer(transaction_item)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        transaction_item = self.get_object(pk)
        serializer = TransactionSerializer(transaction_item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PossessionTitleList(APIView):
    def get(self, request, format=None):
        posse = PossessionTitle.objects.all()
        serializer = PossessionTitleSerializer(posse, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = PossessionTitleSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PossessionTitleDetail(APIView):
    def get_object(self, pk):
        try:
            return PossessionTitle.objects.get(pk=pk)
        except PossessionTitle.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        posse = self.get_object(pk)
        serializer = PossessionTitleSerializer(posse)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        posse = self.get_object(pk)
        serializer = PossessionTitleSerializer(posse, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TitleAttrList(APIView):
    def get(self, request, format=None):
        attributs = TitleAttr.objects.all()
        serializer = TitleAttrSerializer(attributs, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = TitleAttrSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TitleAttrDetail(APIView):
    def get_object(self, pk):
        try:
            return TitleAttr.objects.get(pk=pk)
        except TitleAttr.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        titleattr = self.get_object(pk)
        serializer = TitleAttrSerializer(titleattr)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        titleattr = self.get_object(pk)
        serializer = TitleAttrSerializer(titleattr, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InfoPossessionList(APIView):
    def get(self, request, format=None):
        info_possession = InfoPossession.objects.all()
        serializer = InfoPossessionSerializer(info_possession, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = InfoPossessionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InfoPossessionDetail(APIView):
    def get_object(self, pk):
        try:
            return InfoPossession.objects.get(pk=pk)
        except InfoPossession.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        info_possession = self.get_object(pk)
        serializer = InfoPossessionSerializer(info_possession)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        info_possession = self.get_object(pk)
        serializer = InfoPossessionSerializer(info_possession, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        info_possession = self.get_object(pk)
        info_possession.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@transaction.atomic
def make_update(conta1, conta2, valor):
    account1 = Account.objects.get(pk=conta1)
    dest_transfer = Account.objects.get(pk=conta2)
    transfer1 = Transactions(transaction='W', update_account=account1, dest_account=dest_transfer, value=valor)
    transfer2 = Transactions(transaction='D', update_account=dest_transfer, dest_account=account1, value=valor)
    account1.balance -= Decimal(valor)
    dest_transfer.balance += Decimal(valor)
    account1.save()
    dest_transfer.save()
    transfer1.save()
    transfer2.save()
    return transfer1
