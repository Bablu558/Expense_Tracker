from django.urls import path
from . import views
from .views import register, login_view, logout_view
from .views import profile
urlpatterns = [
    path('', views.home, name='home'),
    path('expenses/', views.expense_list, name='expense_list'),
    path('add-expense/', views.add_expense, name='add_expense'),
    path('delete-expense/<int:id>/', views.delete_expense, name='delete_expense'),
    # path('profile/', views.profile, name='profile'),
    path('profile/', profile, name='profile'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('add_borrow/', views.add_borrow, name='add_borrow'),
    path('delete_borrow/<int:borrow_id>/', views.delete_borrow, name='delete_borrow'),
    path('borrow-list/', views.borrow_list, name='borrow_list'),
]
