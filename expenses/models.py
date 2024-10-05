from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
class Expense(models.Model):
    CATEGORY_CHOICES = [
        ('Food', 'Food'),
        ('Travel', 'Travel'),
        ('Shopping', 'Shopping'),
        ('Entertainment', 'Entertainment'),
        ('Grocery', 'Grocery'),
        ('College', 'College'),
        ('Other', 'Other'),
    ]
    
    title = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    date = models.DateField(default=timezone.now)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.title} - {self.amount}"


class Borrow(models.Model):
    borrower_name = models.CharField(max_length=100)
    purpose = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_borrowed = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.borrower_name} - {self.amount} on {self.date_borrowed}"