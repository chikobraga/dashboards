from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from app.models import Account, Transactions


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
        template = loader.get_template('app/plain_page.html')
        number = Account.objects.get(pk=number)
        transacao = Transactions.objects.filter(update_account=number).order_by('id')
        context = {
        'number': number,
        'transacao': transacao,
    }
    except Board.DoesNotExist:
        raise Http404
    return HttpResponse(template.render(context, request))
