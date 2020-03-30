from django.contrib import admin
from .models import Account, Transactions, PossessionTitle, TitleAttr

# Register your models here.

admin.site.register(Account)
admin.site.register(Transactions)
admin.site.register(PossessionTitle)
admin.site.register(TitleAttr)
