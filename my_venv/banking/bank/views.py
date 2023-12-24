from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import os
from django.http import HttpResponseRedirect, HttpResponse
from .models import Account, UserProfile, Transaction, UserMessage
from .forms import TransactionForm, UserMessageForm
from . import forms

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('../homepage/')
        else:
            messages.success(request, ("there was an error logging in, try again..."))
            return HttpResponseRedirect('../login_user/')
    else:
        return render(request, 'registration/login_user.html', {})


def homepage(request):
    user_profile = UserProfile.objects.get(user=request.user)
    account = Account.objects.get(user=user_profile)
    return render(request, "bank/homepage.html", {'user_profile': user_profile, 'account': account})


def home(request):
    return render(request, "registration/home.html")

def intro(request):
    return render(request, "bank/intro.html")


def success(request):
    var1 = UserProfile.objects.get(user=request.user)
    var2 = Account.objects.get(user=var1)
    last_transaction = Transaction.objects.order_by('-date').first()
    if last_transaction:
        transaction_data = {
        'amount': last_transaction.amount,
        'description': last_transaction.description,
        'date': last_transaction.date,
        'beneficiary_first_name' : last_transaction.beneficiary_first_name,
        'beneficiary_account_number' : last_transaction.beneficiary_account_number,
    }
    else:
        transaction_data = None

    return render(request, 'bank/success.html', {'transaction_data': transaction_data, 'user_profile': var1, 'account': var2})

def history(request):
    transactions = Transaction.objects.order_by('-date')
    return render(request, 'bank/history.html', {'transactions': transactions})

    

def mycards(request):
    return render(request, 'bank/mycards.html')


def sent(request):
    var1 = UserProfile.objects.get(user=request.user)
    last_message = UserMessage.objects.order_by('-timestamp').first()
    if last_message:
        message_data = {
        'message': last_message.message,
        'title': last_message.title,
    }
    else:
        message_data = None

    return render(request, 'bank/sent.html', {'user_profile': var1,'message_data': message_data})

    


def profile(request):
    var1 = UserProfile.objects.get(user=request.user)
    var2 = Account.objects.get(user=var1)
    return render(request, "bank/profile.html", {'user_profile': var1, 'account': var2})



def transact(request):
    user_profile = UserProfile.objects.get(user=request.user)
    account = Account.objects.get(user=user_profile)
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            beneficiary_first_name = form.cleaned_data['beneficiary_first_name']
            beneficiary_account_number = form.cleaned_data['beneficiary_account_number']
            amount = form.cleaned_data['amount']
            description = form.cleaned_data['description']

            try:
                beneficiary_account = Account.objects.get(account_number=beneficiary_account_number)
            except Account.DoesNotExist:
                messages.success(request, ("Beneficiary account not found. Please check the account number."))
                return HttpResponseRedirect('../transact/')
            else:
                if account.balance >= amount:
                    account.balance -= amount
                    beneficiary_account.balance += amount
                    account.save()
                    beneficiary_account.save()
                    Transaction.objects.create(
                        beneficiary_first_name=beneficiary_first_name,
                        beneficiary_account_number=beneficiary_account_number,
                        owner=account,
                        amount=amount,
                        description=description,  # You can modify this accordingly
                    )
                    return HttpResponseRedirect('../success/')
                else:
                    messages.success(request, ("Insufficiant balance. Please enter a valid amount."))
    else:
        form = TransactionForm()

    return render(request, 'bank/transact.html', {'form': form})




# views.py
def message(request):
    owner = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        form = UserMessageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            message = form.cleaned_data['message']

            UserMessage.objects.create(title=title,message=message,owner=owner)
            return HttpResponseRedirect('../sent/')
    else:
        form = UserMessageForm()
    
    return render(request, 'bank/message.html', {'form': form})
