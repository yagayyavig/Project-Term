# Main flask backend 
# Term 2 handle this 

from flask import Flask, render_template, request, redirect, url_for
from db import db
from models.expense import Expense
from sqlalchemy import select
from datetime import datetime
from pathlib import Path

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///store.db"
app.instance_path = Path(".").resolve()

db.init_app(app)

with app.app_context():
    from models import expense
    db.create_all()

# Home Page
@app.route("/")
def home():
    stmt = db.select(Expense)
    expenses = db.session.execute(stmt).scalars().all()
    return render_template("home.html", expenses=expenses)

# List All Expenses
@app.route("/expenses")
def list_expenses():
    sort = request.args.get("sort")
    stmt = db.select(Expense)

    if sort == "amount":
        stmt = stmt.order_by(Expense.amount)
    elif sort == "date":
        stmt = stmt.order_by(Expense.date)
    elif sort == "category":
        stmt = stmt.order_by(Expense.category)

    expenses = db.session.execute(stmt).scalars().all()
    return render_template("expenses.html", expenses=expenses)

# Add Expense
@app.route("/expenses/add", methods=["GET", "POST"])
def add_expense():
    if request.method == "POST":
        amount = float(request.form["amount"])
        category = request.form["category"]
        date = datetime.strptime(request.form["date"], "%Y-%m-%d").date()
        note = request.form["note"]

        today = datetime.today().date()

        if date > today:
            return render_template("error.html", message="Cannot add expense for a future date!")

        new_expense = Expense(amount=amount, category=category, date=date, note=note)
        db.session.add(new_expense)
        db.session.commit()
        return redirect(url_for("list_expenses"))
    
    today = datetime.today().strftime('%Y-%m-%d')
    return render_template("add_expense.html", today=today)


# Need to do 

# Edit Expense


# Take you to confirm delete (this dosnt delete anything, just takes you to the confim page)
@app.route("/expenses/<int:expense_id>/deleteconfirm")
def confirm_delete(expense_id):
    stmt = select(Expense).where(Expense.id == expense_id)
    expense = db.session.execute(stmt).scalars().first()

    # this if statment checks that the expense actally exists 
    if not expense:
        return render_template("error.html", message= "No expence matching the ID")
    
    return render_template("confirm_delete.html", expense=expense)


# Actally Delete Expense
@app.route("/expenses/<int:expense_id>/delete", methods=["POST"])
# choose what expense to delete based on unique id
def delete_expense(expense_id):
    stmt = select(Expense).where(Expense.id == expense_id)
    expense = db.session.execute(stmt).scalars().first()

    # this if statment checks that the expense actally exists 
    if not expense:
        return render_template("error.html", message= "No expence matching the ID")
    
    # this deletes the chosen expense and commits the changes 
    db.session.delete(expense)
    db.session.commit()
    # return back to expeses page after deletion
    return redirect(url_for('list_expenses'))

if __name__ == "__main__":
    app.run(debug=True, port=8002)
