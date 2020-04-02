from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import F
from decimal import Decimal
from app.models import *
from app.forms import *

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

            transfer1 = Transactions(transaction='W',update_account=account1,dest_account=dest_transfer, value=value_rec)
            teste = account1.balance = account1.balance + Decimal(value_rec)
            teste.save()
            transfer2 = Transactions(transaction='D', update_account=dest_transfer, dest_account=account1,value=value_rec)
            transfer1 = transfer1.save()
            transfer2 = transfer2.save()
            #return redirect('account/%s' % number)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        template = loader.get_template('app/plain_page.html')
        number = Account.objects.get(pk=number)
        others_c = Account.objects.all()
        p_attr = TitleAttr.objects.all()
        p_info = InfoPossession.objects.all()
        p_title = PossessionTitle.objects.filter(owner_title=number)
        transacao = Transactions.objects.filter(update_account=number).order_by('id')
        context = {
        'number': number,
        'transacao': transacao,
        'others_c' : others_c,
        'p_title' : p_title,
        'p_attr' : p_attr,
        'p_info' : p_info,
    }
    except Board.DoesNotExist:
        raise Http404
    return HttpResponse(template.render(context, request))
