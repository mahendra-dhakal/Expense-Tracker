Django Expense Tracker API
A REST API for tracking personal expenses and income with JWT authentication and automatic tax calculations.

Features includes :
1.JWT Authentication(register, login, refresh)
2.Auto Tax calculations (flat or percentage)
3.User data isolation 
4.Superuser can see all data
5.Pagination


My Approach:
Used django's built in User model and created a ExpenseIncome model
Implemented tax calculation as a model property rather than storing it in the database
Used JWT  tokens for Authentication 


Setup Instructions

#Prerequisites:
Python 3.8+
pip package manager

#Installation

Clone and setup project:

git clone https://github.com/mahendra-dhakal/Expense-Tracker.git
virtualenv env
env\scripts\activate
pip install -r requirements.txt
cd expensetracker


Database setup:

python manage.py makemigrations
python manage.py migrate

Create superuser:

python manage.py createsuperuser

Run server
python manage.py runserver
