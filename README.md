# (CLI) Expense Tracker Application

A feature-packed, interactive Command-Line Interface (CLI) Expense Tracker built in Python. Designed to help users manage, organize, analyze, and track their daily expenses directly from the terminal with real-time feedback, colored visuals, and file persistence.

---

## Author & Internship Details

* **Name:** Samiullah
* **Registration Number:** `CX-INT-2026-PY-0057`

---

## Features Implemented

* **Add & Categorize Expenses:** Record expenses with description, amount, category selection, and automatic timestamp generation (`YYYY-MM-DD HH:MM`).
* **Detailed Expense Views:** Tabular layout displaying all expenses with auto-calculated total expenditure.
* **Category Summary & Breakdown:** Dynamic breakdown showing total spent and percentage distribution across categories (`Food`, `Transport`, `Shopping`, `Bills`, `Other`).
* **Category Filtering:** Easily isolate and inspect expenses within a specific category.
* **Edit Existing Expense:** Flexible record modification by ID — press `Enter` to keep existing values or update specific fields.
* **Safe Delete:** Remove records by ID with interactive confirmation dialogs.
* **Sorting Capabilities:** Sort records by Amount (Low to High / High to Low) or Date (Oldest / Newest).
* **Monthly Budgeting & Alerts:** Set a monthly budget target with real-time indicators and automatic warning alerts when overspending occurs.
* **Monthly Analytics & Trends:** Deep-dive monthly breakdown highlighting highest/lowest spending months and average transaction metrics.
* **CSV Exporting:** Export all records into timestamped CSV files (`expenses_export_YYYYMMDD_HHMMSS.csv`).
* **Data Persistence:** File I/O operations saving/loading data automatically using `expenses.txt`.
* **Visual Terminal UI:** Enhanced with `colorama` ANSI color formatting and `pyfiglet` ASCII art banners.

---

## Requirements & Installation:

### Prerequisites:
* **Python:** `3.10+` recommended

### 1. Clone the Repository:
```bash
git clone [https://github.com/your-username/expense-tracker.git](https://github.com/your-username/expense-tracker.git)
cd expense-tracker
```

### 2. Install Required Dependencies:
Install the required packages using pip:

```bash
pip install colorama pyfiglet
```
---

## How to Run the Application:
Execute the Python script directly in your terminal:

```bash
python expense_tracker.py
```

Follow the interactive numbered on-screen menu (1-12) to navigate through the application features.

## Project Structure:

```bash
expense_tracker/
├── expense_tracker.py       # Main application file
├── expenses.txt             # Data storage file (auto-created)
├── README.md                # Project description
└── Screenshots/
    ├── main_menu.png        # Screenshot of menu
    └── expense_list.png     # Screenshot of expense list
```