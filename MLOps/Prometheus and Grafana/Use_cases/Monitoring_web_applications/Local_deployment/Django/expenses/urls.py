from django.urls import path
from expenses import views

urlpatterns = [
       path('', views.home, name='home'),
       path('expenses/', views.expenses_list, name='expenses_list'),
       path('approve-expense/<int:expense_id>/', views.approve_expense, name='approve_expense'),
]