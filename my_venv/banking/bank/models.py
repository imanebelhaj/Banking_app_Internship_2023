from django.db import models
from django.contrib.auth.models import User
import datetime

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    address = models.TextField()
    phone_number = models.CharField(max_length=15)
    def __str__(self):
        return f"{self.user.username}'s Profile"


class Account(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    RIB = models.CharField(max_length=20, unique=True)
    account_number = models.CharField(max_length=20, unique=True)
    balance = models.DecimalField(max_digits=12, decimal_places=2)
    def __str__(self):
        return self.account_number


class Transaction(models.Model):
    beneficiary_first_name = models.CharField(max_length=100)
    beneficiary_account_number = models.CharField(max_length=100)
    owner = models.ForeignKey(Account, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(default=datetime.datetime.now)
    def __str__(self):
        return f"Transaction from {self.owner.user.user.username} to {self.beneficiary_first_name}"
    


class UserMessage(models.Model):
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Message from {self.owner.user.user.username}: {self.title}"
