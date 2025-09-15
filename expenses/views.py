from django.shortcuts import render, redirect, get_object_or_404
from .models import Expense
from .forms import ExpenseForm
from .models import Borrow
from .forms import BorrowForm
from django.db.models import Sum, Q
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm, LoginForm 
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'home.html')

@login_required
def profile(request):
    user = request.user
    context = {
        'user': user
    }
    return render(request, 'profile.html', context)

@login_required
def expense_list(request):
    category = request.GET.get('category')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    search_term = request.GET.get('search')

    expenses = Expense.objects.filter(user=request.user).order_by('-date')  # ✅ Filter by logged-in user

    if category:
        expenses = expenses.filter(category=category)
    if start_date and end_date:
        expenses = expenses.filter(date__range=[start_date, end_date])
    if search_term:
        expenses = expenses.filter(
            Q(title__icontains=search_term) |
            Q(description__icontains=search_term)
        )

    total_expense = sum(expense.amount for expense in expenses)
    context = {
        'expenses': expenses,
        'total_expense': total_expense,
        'category': category,
        'start_date': start_date,
        'end_date': end_date,
        'search_term': search_term,
    }
    return render(request, 'expenses/expense_list.html', context)

@login_required
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user  # ✅ Assign logged-in user
            expense.save()
            return redirect('expense_list')
    else:
        form = ExpenseForm()
    return render(request, 'expenses/add_expense.html', {'form': form})

@login_required
def delete_expense(request, id):
    expense = get_object_or_404(Expense, id=id, user=request.user)  # ✅ Ensure user owns expense
    expense.delete()
    return redirect('expense_list')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def add_borrow(request):
    if request.method == 'POST':
        form = BorrowForm(request.POST)
        if form.is_valid():
            borrow = form.save(commit=False)
            borrow.user = request.user
            borrow.save()
            return redirect('borrow_list')
    else:
        form = BorrowForm()
    return render(request, 'add_borrow.html', {'form': form})

@login_required
def delete_borrow(request, borrow_id):
    borrow = Borrow.objects.get(id=borrow_id, user=request.user)
    if request.method == 'POST':
        borrow.delete()
        return redirect('borrow_list')
    return render(request, 'confirm_delete.html', {'borrow': borrow})

@login_required
def borrow_list(request):
    borrows = Borrow.objects.filter(user=request.user)

    borrower_name = request.GET.get('borrower_name', '')
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')

    if borrower_name:
        borrows = borrows.filter(borrower_name__icontains=borrower_name)
    if start_date:
        borrows = borrows.filter(date_borrowed__gte=start_date)
    if end_date:
        borrows = borrows.filter(date_borrowed__lte=end_date)

    total_amount_borrowed = borrows.aggregate(Sum('amount'))['amount__sum'] or 0

    return render(request, 'borrow_list.html', {
        'borrows': borrows,
        'total_amount_borrowed': total_amount_borrowed,
        'borrower_name': borrower_name,
        'start_date': start_date,
        'end_date': end_date,
    })
