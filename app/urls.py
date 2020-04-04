from django.urls import path, re_path, include
from rest_framework.urlpatterns import format_suffix_patterns
from app import views

urlpatterns = [
    # Matches any html file - to be used for gentella
    # Avoid using your .html in your resources.
    # Or create a separate django app.
    re_path(r'^.*\.html', views.gentella_html, name='gentella'),

    # The home page
    path('', views.index, name='login'),
    path('account/<int:number>/', views.Account_html, name='accountnumber'),
    path('api/account/', views.AccountList.as_view()),
    path('api/account/<int:pk>/', views.AccountDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)