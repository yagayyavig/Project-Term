# Main flask backend 
# Term 2 handle this 

from flask import Flask, render_template, request, redirect, url_for
from db import db
from models.expense import Expense
from models.category import Category
from sqlalchemy import select
from datetime import datetime
from pathlib import Path

def create_app(test_config=None):
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///store.db"
    app.instance_path = Path(".").resolve()

    if test_config:
            app.config.update(test_config)

    db.init_app(app)

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

        if sort =="id":
            stmt= stmt.order_by(Expense.id)
        elif sort == "amount":
            stmt = stmt.order_by(Expense.amount)
        elif sort == "date":
            stmt = stmt.order_by(Expense.date)
        elif sort == "category":
            stmt = (select(Expense).join(Expense.category).order_by(Category.name))

        expenses = db.session.execute(stmt).scalars().all()
        return render_template("expenses.html", expenses=expenses)

    # Add Expense
    @app.route("/expenses/add", methods=["GET"])
    def add_expense_form():
        categories = db.session.execute(select(Category)).scalars().all()
        today = datetime.today().strftime('%Y-%m-%d')
        return render_template("add_expense.html", today=today, categories=categories)

    @app.route("/expenses/add", methods=["POST"])
    def add_expense():
        amount = float(request.form["amount"])
        category_id = int(request.form["category_id"])
        date = datetime.strptime(request.form["date"], "%Y-%m-%d").date()
        note = request.form["note"]

        today = datetime.today().date()
        if date > today:
            return render_template("error.html", message="Cannot add expense for a future date!")
        
        stmt = select(Category).where(Category.id == category_id)
        category = db.session.execute(stmt).scalars().first()

        new_expense = Expense(amount=amount, category=category, date=date, note=note)

        db.session.add(new_expense)
        db.session.commit()
        return redirect(url_for("list_expenses"))


    # Shows the "Edit" Form
    @app.route("/expenses/edit/<int:expense_id>", methods=["GET"])
    def edit_form(expense_id):
        stmt = select(Expense).where(Expense.id == expense_id)
        expense = db.session.execute(stmt).scalars().first()

        if not expense:
            return render_template("error.html", message="No expense matching the ID")
        
        categories = db.session.execute(select(Category)).scalars().all() 
        today = datetime.today().strftime("%Y-%m-%d")
        
        return render_template("edit_expense.html", expense=expense, categories=categories, today=today)

    # Edit Expense
    @app.route("/expenses/edit/<int:expense_id>", methods=["POST"])
    def edit_expense(expense_id):
        stmt = select(Expense).where(Expense.id == expense_id)
        expense = db.session.execute(stmt).scalars().first()

        if not expense:
            return render_template("error.html", message="No expense matching the ID")
        
        amount = float(request.form["amount"])
        category_id = int(request.form["category_id"])
        date = datetime.strptime(request.form["date"], "%Y-%m-%d").date()
        note = request.form["note"]
        
        today = datetime.today().date()
        if date > today:
            return render_template("error.html", message="Cannot set a future date for the expense")
        
        stmt1 =  select(Category).where(Category.id == category_id)
        category = db.session.execute(stmt1).scalars().first()
        if not category:
            return render_template("error.html", message="Invalid category selected")

        expense.amount = amount
        expense.category = category
        expense.date = date
        expense.note = note

        db.session.commit()
        return redirect(url_for("list_expenses"))

    # Take you to confirm delete (this doesn't delete anything, just takes you to the confirm page)
    @app.route("/expenses/<int:expense_id>/deleteconfirm")
    def confirm_delete(expense_id):
        stmt = select(Expense).where(Expense.id == expense_id)
        expense = db.session.execute(stmt).scalars().first()

        # this if statement checks that the expense actually exists 
        if not expense:
            return render_template("error.html", message= "No expense matching the ID")
        
        return render_template("confirm_delete.html", expense=expense)


    # Actually Delete Expense
    @app.route("/expenses/<int:expense_id>/delete", methods=["POST"])
    # choose what expense to delete based on unique id
    def delete_expense(expense_id):
        stmt = select(Expense).where(Expense.id == expense_id)
        expense = db.session.execute(stmt).scalars().first()

        # this if statement checks that the expense actually exists 
        if not expense:
            return render_template("error.html", message= "No expense matching the ID")
        
        # this deletes the chosen expense and commits the changes 
        db.session.delete(expense)
        db.session.commit()
        # return back to expenses page after deletion
        return redirect(url_for('list_expenses'))
    

    @app.route("/expenses/category/<int:category_id>")
    def expenses_by_category(category_id):
        category = db.session.get(Category, category_id)
        if not category:
            return render_template("error.html", message="Category not found.")

        sort = request.args.get("sort")
        stmt = select(Expense).where(Expense.category_id == category_id)

        if sort == "id":
            stmt = stmt.order_by(Expense.id)
        elif sort == "amount":
            stmt = stmt.order_by(Expense.amount)
        elif sort == "date":
            stmt = stmt.order_by(Expense.date)

        expenses = db.session.execute(stmt).scalars().all()
        return render_template("expenses_by_category.html", expenses=expenses, category=category)


    
    return app

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        from models import expense, category
        db.create_all()

        # Create Default Categories
        default_categories = [
        "Dining Out 🍽️",
        "Education 🎓",
        "Entertainment 🎬",
        "Gas ⛽",
        "Groceries 🛒",
        "Health & Medical 💊",
        "Internet & Phone 📶",
        "Personal Care 🧴",
        "Rent 🏠",
        "Transport 🚌",
        "Utilities 💡",
        "Other 📁"
    ]

        for name in default_categories:
            exists = db.session.execute(
                select(Category).where(Category.name == name)
            ).scalars().first()

            if not exists:
                db.session.add(Category(name=name))
        db.session.commit()
        
    app.run(debug=True, port=8002)
