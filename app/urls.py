from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('transactions', views.transactions, name='transactions'),
    path('view_user', views.view_user, name='view_user'),
    path('make_transaction', views.make_transaction, name='make_transaction'),
]
