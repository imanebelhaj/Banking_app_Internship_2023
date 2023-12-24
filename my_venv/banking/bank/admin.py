from django.contrib import admin
from .models import UserProfile, Account,UserMessage,Transaction


admin.site.register(UserProfile)
admin.site.register(Account)
admin.site.register(UserMessage)
admin.site.register(Transaction)