# Project Term - Budget Tracker
## Yagayya Vig, Shrey Dhand, Luis Morin, Samantha Lum & Nick Fiebelkorn
changes
---

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
Sprint 2 builds on that by adding front-end features, better UX, and category filters.

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

## Sprint 2 - Deliverables (Week 2)

**Main Goal:**  
Enhance functionality and design by implementing sorting, editing, deleting, and filtering by category.

### Features Completed in Sprint 2:

- `add_expense.html` and `edit_expense.html` templates finalized
- `expenses.html` implemented with table view of all expenses
- Edit and delete functionality added and tested
- Error handling (`error.html`) created
- Dynamic category filter on `/expenses?category=Food`, etc.
- Sorting options by `amount`, `date`, and `category` with filter buttons
- Category dropdown added to the Add Expense form
- Minor UI improvements and CSS refinements for responsiveness
- Reorganized routes for modularity and clarity
- Validations enhanced: No empty fields, valid categories, etc.
- Improved error display with flash messages

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

# Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install required packages
pip install -r requirements.txt

# Run the app
python app.py
