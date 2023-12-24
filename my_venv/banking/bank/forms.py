from django import forms
from .models import Transaction


class TransactionForm(forms.ModelForm):
   class Meta:
        model = Transaction
        fields = ['beneficiary_first_name', 'beneficiary_account_number', 'amount', 'description']
        widgets = {
           'beneficiary_first_name': forms.TextInput(attrs={'class': 'custom-input'}),
           'beneficiary_account_number': forms.TextInput(attrs={'class': 'custom-input'}),
            'amount': forms.TextInput(attrs={'class': 'custom-input'}),
            'description': forms.TextInput(attrs={'class': 'custom-input'}),
        }
   
class UserMessageForm(forms.Form):
    title = forms.CharField(max_length=255)
    message = forms.CharField(widget=forms.Textarea)