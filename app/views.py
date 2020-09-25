from django.contrib import messages
from django.shortcuts import render, redirect
from . import models


#  Render Home Page
def home(request):
    users = models.UserInfo.objects.all().order_by('uid')
    context = {'userinfo': users}
    return render(request, 'home.html', context=context)


#  Render Transactions page
def transactions(request):
    transactions = models.Transaction.objects.all().order_by('-date')
    context = {'transactions': transactions}
    return render(request, 'transactions.html', context=context)


#  Render User page
def view_user(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        user_info = models.UserInfo.objects.get(name=name)
        users = models.UserInfo.objects.all().exclude(name=user_info)
        context = {'user_info': user_info, 'users': users}
        return render(request, 'user.html', context=context)
    return redirect('/')


#  Performs Transaction
def make_transaction(request):
    if request.method == 'POST':
        sender = request.POST.get('sender')
        receiver = request.POST.get('receiver')
        credits = int(request.POST.get('credits'))

        user_info = models.UserInfo.objects.get(name=sender)
        users = models.UserInfo.objects.all().exclude(name=user_info)
        context = {'user_info': user_info, 'users': users}

        if sender == receiver:
            messages.warning(request, 'You can\'t send to yourself')
            return render(request, 'user.html', context=context)

        sender_obj = models.UserInfo.objects.get(name=sender)
        receiver_obj = models.UserInfo.objects.get(name=receiver)

        if 0 <= sender_obj.credit < credits:
            messages.warning(request, 'You don\'t have enough credits')
            return render(request, 'user.html', context=context)

        if credits <= 0:
            messages.warning(request, 'Invalid credits')
            return render(request, 'user.html', context=context)

        sender_obj.credit -= credits
        receiver_obj.credit += credits

        sender_obj.save()
        receiver_obj.save()

        transaction_obj = models.Transaction(sender=sender, receiver=receiver, credit=credits)
        transaction_obj.save()

        user_info = models.UserInfo.objects.get(name=sender)
        users = models.UserInfo.objects.all().exclude(name=user_info)
        context = {'user_info': user_info, 'users': users}

        messages.info(request, 'Transaction Success')
        return render(request, 'user.html', context=context)

    messages.warning(request, 'Transaction Failed')
    return redirect('/')


def adduser(request):
    return render(request, 'adduser.html')


def create_user(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        credits = int(request.POST.get('credits'))

        if models.UserInfo.objects.filter(name=name).exists():
            messages.warning(request, 'User Name already exists')
            return redirect('adduser')

        if credits <= 0:
            messages.warning(request, 'Invalid Credits')
            return redirect('adduser')

        user_obj = models.UserInfo(
            name=name,
            email=email,
            credit=credits
        )
        user_obj.save()

        messages.info(request, 'User Successfully added')
        return redirect('/')

    messages.warning(request, 'User Add failed')
    return redirect('adduser')
