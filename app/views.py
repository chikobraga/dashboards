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
    context = {}
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
            account = request.POST.get('account')
            op_name = request.POST.get('op_name')
            value_rec = request.POST.get('value')

            account1 = Account.objects.get(pk=account)
            dest_transfer = Account.objects.get(pk=op_name)

            transfer1 = Transactions(transaction='W', update_account=account1, dest_account=dest_transfer,
                                     value=value_rec)
            account1.balance -= Decimal(value_rec)
            account1.save()
            transfer2 = Transactions(transaction='D', update_account=dest_transfer, dest_account=account1,
                                     value=value_rec)
            dest_transfer.balance += Decimal(value_rec)
            dest_transfer.save()
            transfer1 = transfer1.save()
            transfer2 = transfer2.save()
            # return redirect('account/%s' % number)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        template = loader.get_template('app/plain_page.html')
        naccount = Account.objects.get(pk=number)
        if PossessionTitle.objects.filter(owner_title=number):
            totalp = PossessionTitle.objects.filter(owner_title=number).aggregate(patrimony=Sum('value'))
        finalsum = naccount.balance + totalp['patrimony']
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
            'naccount': naccount,
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
            serializer.save()
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
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.erros, status=status.HTTP_400_BAD_REQUEST)

