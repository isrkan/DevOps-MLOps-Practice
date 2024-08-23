from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__) # Initialize the Flask application

@app.route('/') # Define the home route
def home():
    return render_template('index.html')

@app.route('/expenses')
def expenses():
    """
    Display a list of expenses.
    """
    with open('data/expenses.json') as f:
        expenses = json.load(f)
    return render_template('expenses.html', expenses=expenses)

@app.route('/add_expense', methods=['GET', 'POST'])
def add_expense():
    """
    Add a new expense.

    GET: Renders 'add_expense.html' form.
    POST: Processes form data, adds new expense to 'data/expenses.json', and redirects to '/expenses'.
    """
    if request.method == 'POST':
        # Create a new expense object from form data
        new_expense = {
            'amount': request.form['amount'],
            'category': request.form['category'],
            'description': request.form['description'],
            'approved': request.form.get('approved') == 'on',
            'added_by': request.form['added_by']
        }
        # Load current expenses, append new expense, and save back to JSON file
        with open('data/expenses.json', 'r+') as f:
            expenses = json.load(f)
            new_expense['id'] = len(expenses) + 1 # Assign a new ID to the expense
            expenses.append(new_expense)
            f.seek(0)
            json.dump(expenses, f, indent=4)
        return redirect(url_for('expenses'))  # Redirect to expenses page after adding expense
    return render_template('add_expense.html')  # Render the add expense form for GET requests

@app.route('/edit_expense/<int:id>', methods=['GET', 'POST'])
def edit_expense(id):
    """
    Edit an existing expense.

    GET: Renders 'edit_expense.html' form with expense details.
    POST: Updates expense details in 'data/expenses.json' and redirects to '/expenses'.
    """
    # Load expense data from JSON file and find the expense to edit by ID
    with open('data/expenses.json') as f:
        expenses = json.load(f)
    expense = next((exp for exp in expenses if exp['id'] == id), None)
    if request.method == 'POST':
        # Update expense details from form data
        expense['amount'] = request.form['amount']
        expense['category'] = request.form['category']
        expense['description'] = request.form['description']
        expense['approved'] = request.form.get('approved') == 'on'
        expense['added_by'] = request.form['added_by']
        # Save updated expenses list back to JSON file
        with open('data/expenses.json', 'w') as f:
            json.dump(expenses, f, indent=4)
        return redirect(url_for('expenses'))  # Redirect to expenses page after editing expense
    return render_template('edit_expense.html', expense=expense)  # Render the edit expense form for GET requests

@app.route('/delete_expense/<int:id>', methods=['POST'])
def delete_expense(id):
    """
    Delete an expense.

    POST: Deletes expense from 'data/expenses.json' and redirects to '/expenses'.
    """
    # Load expense data from JSON file and remove expense with matching ID
    with open('data/expenses.json') as f:
        expenses = json.load(f)
    expenses = [expense for expense in expenses if expense['id'] != id]
    # Save updated expenses list back to JSON file
    with open('data/expenses.json', 'w') as f:
        json.dump(expenses, f, indent=4)
    return redirect(url_for('expenses'))  # Redirect to expenses page after deleting expense


if __name__ == '__main__':
    app.run(debug=True, port=5000) # Run the Flask app