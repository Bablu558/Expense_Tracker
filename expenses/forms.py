from django import forms
from .models import Expense
from .models import Borrow
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['amount', 'category', 'date', 'description']



class BorrowForm(forms.ModelForm):
    class Meta:
        model = Borrow
        fields = ['borrower_name', 'purpose', 'amount', 'date_borrowed']
        widgets = {
            'date_borrowed': forms.DateInput(attrs={'type': 'date'}),
        }