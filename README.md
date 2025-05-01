<<<<<<< HEAD
# Project Term - Budget Tracker
## Yagayya Vig, Shrey Dhand, Luis Morin, Samantha Lum & Nick Fiebelkorn

 
=======
# Project Term - Expense Tracker

## Team Members
- Yagayya Vig
- Shrey Dhand
- Luis Morin
- Nick Fiebelkorn
- Samantha Lum

---

## Project Overview

Expense Tracker is a simple Flask-based web application designed to help users manage their personal expenses.  
Users can add, view, sort, edit, and delete their expenses easily through a clean dark-themed interface.  
This project is built with Flask, SQLAlchemy 2.0, and a responsive front-end designed for both desktop and mobile use.

The project is divided into multiple sprints following Agile methodology.  
Sprint 1 focused on building the core backend and basic functionality of the app.

---

## Sprint 1 - Deliverables

**Main Goal:**  
Create the Minimum Viable Product (MVP) that supports basic expense management with a working backend, database connection, and simple front-end structure.

### Features Completed in Sprint 1:

- Flask app setup (`app.py`)
- SQLite database integration with SQLAlchemy 2.0
- Expense model (`Expense`) created
- Home route (`/`) listing all expenses
- Expenses listing route (`/expenses`)
- Add expense route (`/expenses/add`)
- Future date validation for adding expenses
- Basic dark-themed CSS styling
- Project folder structure organized:
  - `/models`
  - `/templates`
  - `/static/css`
- Local development running on `localhost:8002`
- Initial GitHub repository setup (with commits showing sprint progress)

---

## Remaining Sprint 1 Tasks (assigned to teammates):

- `add_expense.html` template (Add form) 
- `edit_expense.html` template (Edit form) 
- `expenses.html` template (Table to display expenses)
- `error.html` template (Display error messages)
- Edit Expense backend route (`/expenses/<id>`)
- Delete Expense backend route (`/expenses/<id>/delete`)
- CSS style for the app 
---

## Project Technologies

- Python 3.11+
- Flask
- SQLAlchemy 2.0 (ORM)
- SQLite (local database)
- Jinja2 (for templating)
- HTML + CSS 

---

## How to Run Locally

```bash
# Clone the repository
git clone https://github.com/yagayyavig/Project-Term.git
cd expense-tracker

# Requirements to run the project 
pip install Flask 
pip install flask_SQLAlchemy

# Run the app
python app.py
```
