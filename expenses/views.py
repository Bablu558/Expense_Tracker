from django.shortcuts import render, redirect, get_object_or_404
from .models import Expense
from .forms import ExpenseForm
from .models import Borrow
from .forms import BorrowForm
from django.db.models import Sum
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm, LoginForm 
from django.contrib.auth.decorators import login_required
def home(request):
    return render(request, 'home.html')

def profile(request):
    return render(request, 'profile.html')

def expense_list(request):
    # Get filter criteria from request
    category = request.GET.get('category')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    search_term = request.GET.get('search')

    # Start with all expenses
    # expenses = Expense.objects.all()
    
    # agar hum chahe jo newly data h wo top se add ho
    expenses = Expense.objects.all().order_by('-date')  # Order by date descending
    

    # Apply filters if provided
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
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('expense_list')
    else:
        form = ExpenseForm()
    return render(request, 'expenses/add_expense.html', {'form': form})




def delete_expense(request, id):
    expense = get_object_or_404(Expense, id=id)
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
                return redirect('home')  # Redirect to the home page or borrowed amounts page
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')


# View for adding borrow
@login_required
def add_borrow(request):
    if request.method == 'POST':
        form = BorrowForm(request.POST)
        if form.is_valid():
            borrow = form.save(commit=False)
            borrow.user = request.user
            borrow.save()
            return redirect('borrow_list')  # Redirect to list of borrows after adding
    else:
        form = BorrowForm()
    return render(request, 'add_borrow.html', {'form': form})

# View for deleting borrow (after returning money)
def delete_borrow(request, borrow_id):
    borrow = Borrow.objects.get(id=borrow_id, user=request.user)
    if request.method == 'POST':
        borrow.delete()
        return redirect('borrow_list')
    return render(request, 'confirm_delete.html', {'borrow': borrow})

def borrow_list(request):
    # Fetching all borrow entries for the logged-in user
    borrows = Borrow.objects.filter(user=request.user)

    # Getting filter parameters
    borrower_name = request.GET.get('borrower_name', '')
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')

    # Applying filters
    if borrower_name:
        borrows = borrows.filter(borrower_name__icontains=borrower_name)
    if start_date:
        borrows = borrows.filter(date_borrowed__gte=start_date)
    if end_date:
        borrows = borrows.filter(date_borrowed__lte=end_date)

    # Calculating the total amount borrowed (after filters)
    total_amount_borrowed = borrows.aggregate(Sum('amount'))['amount__sum'] or 0

    # Rendering the template with context
    return render(request, 'borrow_list.html', {
        'borrows': borrows,
        'total_amount_borrowed': total_amount_borrowed,
        'borrower_name': borrower_name,
        'start_date': start_date,
        'end_date': end_date,
    })