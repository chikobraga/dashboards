from django.contrib.auth import (login as auth_login, authenticate)
from django.urls import reverse
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.db.models import F, Sum
from decimal import Decimal
from app.models import *
from app.forms import *
from app.serializers import *


def index(request):
    if request.method == 'POST':
        _username = request.POST['username']
        _password = request.POST['password']
        user = authenticate(username=_username, password=_password)
        if user is not None:
            user_id = User.objects.get(username=_username)
            numberaccount = Account.objects.get(user=user_id)
            account = "account/" + str(numberaccount.accountnumber) + "/"
            auth_login(request, user)
            return HttpResponseRedirect(account)
        else:
            _message = 'Invalid login or password, please try again'
    else:
        _message = ''

    context = {'message': _message}
    template = loader.get_template('app/login.html')
    return HttpResponse(template.render(context, request))


def gentella_html(request):
    context = {}
    # The template to be loaded as per gentelella.
    # All resource paths for gentelella end in .html.

    # Pick out the html file name from the url. And load that template.
    load_template = request.path.split('/')[-1]
    template = loader.get_template('app/' + load_template)
    return HttpResponse(template.render(context, request))


def Account_html(request, number):
    try:
        if request.method == 'POST':
            name = request.POST.get('name')
            account = request.POST.get('account')
            op_name = request.POST.get('op_name')
            value_rec = request.POST.get('value')
            if 'maketransfer' == name:
                r_update = make_update(account, op_name, value_rec)
                # return redirect('account/%s' % number)
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        template = loader.get_template('app/plain_page.html')
        number = Account.objects.get(pk=number)
        if PossessionTitle.objects.filter(owner_title=number):
            totalp = PossessionTitle.objects.filter(owner_title=number).aggregate(patrimony=Sum('value'))
            finalsum = number.balance + totalp['patrimony']
        else:
            finalsum = number.balance
        others_c = Account.objects.all()
        p_attr = TitleAttr.objects.all()
        p_info = InfoPossession.objects.all()
        p_title = PossessionTitle.objects.filter(owner_title=number)
        transacao = Transactions.objects.filter(update_account=number).order_by('id')
        context = {
            'number': number,
            'transacao': transacao,
            'others_c': others_c,
            'p_title': p_title,
            'p_attr': p_attr,
            'p_info': p_info,
            'patrimony': finalsum,
        }
    except Board.DoesNotExist:
        raise Http404
    return HttpResponse(template.render(context, request))


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
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


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
        return Response(serializer.erros, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        account = self.get_object(pk)
        account.delte()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TransactionList(APIView):
    def get(self, request, format=None):
        transaction = Transactions.objects.all()
        serializer = TransactionSerializer(transaction, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            account = request.POST.get('update_account')
            op_name = request.POST.get('dest_account')
            value_rec = request.POST.get('value')
            make_update(account, op_name, value_rec)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TransactionDetail(APIView):
    def get_object(self, pk):
        try:
            return Transactions.objects.get(pk=pk)
        except Transactions.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        transaction = self.get_object(pk)
        serializer = TransactionSerializer(transaction)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        transaction = self.get_object(pk)
        serializer = TransactionSerializer(transaction, data=request.data)
        if serializer.is_valid():
            return Response(serializer.data)
        return Response(serializer.erros, status=status.HTTP_400_BAD_REQUEST)


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
        except Transactions.DoesNotExist:
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
        return Response(serializer.erros, status=status.HTTP_400_BAD_REQUEST)


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
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def make_update(conta1, conta2, valor):
    account1 = Account.objects.get(pk=conta1)
    dest_transfer = Account.objects.get(pk=conta2)
    transfer1 = Transactions(transaction='W', update_account=account1, dest_account=dest_transfer, value=valor)
    transfer2 = Transactions(transaction='D', update_account=dest_transfer, dest_account=account1, value=valor)
    account1.balance -= Decimal(valor)
    dest_transfer.balance += Decimal(valor)
    account1.save()
    dest_transfer.save()
    transfer1 = transfer1.save()
    transfer2 = transfer2.save()
    return 'OK'
