from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse
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
            form = TransactionForm(request.POST)
            if form.is_valid():
                pass
                return redirect('account/%s' % number)

        form = TransactionForm()
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
        'form' : form,
    }
    except Board.DoesNotExist:
        raise Http404
    return HttpResponse(template.render(context, request))
