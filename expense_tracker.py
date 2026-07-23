import csv
from datetime import datetime
import os
import shutil
import subprocess
from pyfiglet import Figlet

# expense_tracker.py
# CloudExify Python Internship — Month 1 Project 1
# Samiullah | Registration No: CX-INT-2026-PY-0057


# ==========================================
# Global Variables
# ==========================================
expenses = []
expense_id = 1
monthly_budget = 0.0  # 0.0 means no budget configured
FILE_NAME = "expenses.txt"


# ==========================================
# Terminal & UI Helpers
# ==========================================


def clear_screen():
    command = "cls" if os.name == "nt" else "clear"
    subprocess.run(command, shell=True)


def print_banner():
    columns = shutil.get_terminal_size().columns
    f = Figlet(font="small")
    banner = f.renderText("Expense Tracker")
    for line in banner.splitlines():
        print(line.center(columns))


def display_menu():
    print_banner()
    print("=" * 50)
    print("[1]. Add Expense")
    print("[2]. View Expenses")
    print("[3]. Category summary")
    print("[4]. Filter By Category")
    print("[5]. Delete Expense")
    print("[6]. Set Monthly Budget")
    print("[7]. Export to CSV Format")
    print("[8]. Sort Expenses")
    print("[9]. Save Expenses")
    print("[10]. Save and Exit")
    print("=" * 50)

    # Budget Warning Indicator
    if monthly_budget > 0:
        current_month = datetime.now().strftime("%Y-%m")
        current_month_spent = sum(
            exp["amount"]
            for exp in expenses
            if exp.get("date", "").startswith(current_month)
        )

        print(
            f"📌 Monthly Budget Target: PKR {monthly_budget:,.2f} | Spent: PKR {current_month_spent:,.2f}"
        )

        if current_month_spent > monthly_budget:
            excess = current_month_spent - monthly_budget
            print("=" * 50)
            print(
                f"⚠️  WARNING: You have EXCEEDED your monthly budget by PKR {excess:,.2f}!"
            )
            print("=" * 50)


# ==========================================
# Core Logic Functions
# ==========================================


def set_monthly_budget():
    global monthly_budget
    print("\n--- SET MONTHLY BUDGET ---")
    print(f"Current Target: PKR {monthly_budget:,.2f}")

    while True:
        try:
            val = float(
                input("Enter new monthly budget target (PKR) [0 to disable]: ")
            )
            if val < 0:
                print("Budget target cannot be negative!")
                continue
            monthly_budget = val
            print(
                f"\n✅ Monthly budget target successfully set to PKR {monthly_budget:,.2f}!"
            )
            break
        except ValueError:
            print("Please enter a valid number.")


def add_expense():
    global expense_id

    print("\n--- ADD NEW EXPENSE ---")

    description = input("Description: ").strip()
    while not description:
        print("Description can't be empty!")
        description = input("Description: ").strip()

    while True:
        try:
            amount = float(input("Amount: "))
            if amount <= 0:
                print("Amount can't be zero or negative!")
                continue
            break
        except ValueError:
            print("Please enter a valid number")

    categories = ["Food", "Transport", "Shopping", "Bills", "Other"]
    print("\nCategories:")
    for index, category_name in enumerate(categories, 1):
        print(f"  {index}). {category_name}")

    while True:
        try:
            choice = int(input("Select category (1-5): "))
            if 1 <= choice <= len(categories):
                category = categories[choice - 1]
                break
            print("select from [1-5]!")
        except ValueError:
            print("Enter a valid number!")

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M")

    expense = {
        "id": expense_id,
        "description": description,
        "amount": amount,
        "category": category,
        "date": current_time,
    }

    expenses.append(expense)
    print(
        f"\nExpense added successfully at {current_time}! Assigned ID: {expense_id}"
    )

    # Budget Alert Check on Addition
    if monthly_budget > 0:
        c_month = datetime.now().strftime("%Y-%m")
        this_month_spent = sum(
            e["amount"]
            for e in expenses
            if e.get("date", "").startswith(c_month)
        )
        if this_month_spent > monthly_budget:
            print(
                f"\n⚠️  ALERT: This expense puts you OVER your monthly budget of PKR {monthly_budget:,.2f}!"
            )

    expense_id += 1


def view_expenses(custom_list=None, title="ALL EXPENSES"):
    data_to_show = custom_list if custom_list is not None else expenses

    if not data_to_show:
        print("\nNo Expenses to display!")
        return

    print("\n" + "=" * 70)
    print(f"                --- {title} ---                ")
    print("=" * 70)

    print(
        f"{'ID':<5} {'Date/Time':<18} {'Description':<18} {'Category':<10} {'Amount (PKR)':>12}"
    )
    print("-" * 70)

    total_amount = 0.0

    for exp in data_to_show:
        dt = exp.get("date", "N/A")
        print(
            f"#{exp['id']:<4} {dt:<18} {exp['description']:<18} {exp['category']:<10} {exp['amount']:>12.2f}"
        )
        total_amount += exp["amount"]

    print("-" * 70)
    print(f"{'TOTAL EXPENSE:':<55} PKR {total_amount:>9.2f}")
    print("=" * 70)


def category_summary():

    if not expenses:
        print("\nNo Expenses for now!")
        return

    summary = {}
    grand_total = 0.0

    for exp in expenses:
        cat = exp["category"]
        amt = exp["amount"]

        if cat in summary:
            summary[cat] += amt
        else:
            summary[cat] = amt

        grand_total += amt

    print("\n" + "=" * 45)
    print("            --- CATEGORY SUMMARY ---         ")
    print("=" * 45)
    print(f"{'Category':<15} {'Amount (PKR)':>12} {'Percentage':>12}")
    print("-" * 45)

    for category_name, cat_total in summary.items():
        percentage = (cat_total / grand_total) * 100
        print(
            f"{category_name:<15} "
            f"{cat_total:>12.2f} "
            f"{percentage:>11.1f}%"
        )

    print("-" * 45)
    print(f"{'GRAND TOTAL:':<15} PKR {grand_total:>8.2f}  (100.0%)")
    print("=" * 45)


def filter_by_category():

    if not expenses:
        print("\nNo expenses recorded yet to filter!")
        return

    categories = ["Food", "Transport", "Shopping", "Bills", "Other"]
    print("\nSelect Category to Filter:")
    for index, category_name in enumerate(categories, 1):
        print(f"  {index}). {category_name}")

    while True:
        try:
            choice = int(input("Select category (1-5): "))
            if 1 <= choice <= len(categories):
                selected_category = categories[choice - 1]
                break
            print("Please select a number from 1 to 5!")
        except ValueError:
            print("Please enter a valid number.")

    filtered_expenses = [
        exp for exp in expenses if exp["category"] == selected_category
    ]

    if not filtered_expenses:
        print(f"\n No expenses found under '{selected_category}' category.")
        return

    view_expenses(
        filtered_expenses, title=f"EXPENSES FOR: {selected_category.upper()}"
    )


def sort_expenses():
    if not expenses:
        print("\nNo expenses recorded yet to sort!")
        return

    print("\n--- SORT EXPENSES ---")
    print("[1]. Sort by Amount (Low to High)")
    print("[2]. Sort by Amount (High to Low)")
    print("[3]. Sort by Date (Oldest First)")
    print("[4]. Sort by Date (Newest First)")

    while True:
        choice = input("Select sort option [1-4]: ").strip()
        if choice in ["1", "2", "3", "4"]:
            break
        print("Invalid choice! Select from [1-4].")

    sorted_list = []
    title = ""

    match choice:
        case "1":
            sorted_list = sorted(expenses, key=lambda x: x["amount"])
            title = "EXPENSES (AMOUNT: LOW TO HIGH)"
        case "2":
            sorted_list = sorted(
                expenses, key=lambda x: x["amount"], reverse=True
            )
            title = "EXPENSES (AMOUNT: HIGH TO LOW)"
        case "3":
            sorted_list = sorted(
                expenses, key=lambda x: x.get("date", "")
            )
            title = "EXPENSES (DATE: OLDEST FIRST)"
        case "4":
            sorted_list = sorted(
                expenses, key=lambda x: x.get("date", ""), reverse=True
            )
            title = "EXPENSES (DATE: NEWEST FIRST)"

    view_expenses(sorted_list, title=title)


def delete_expense():

    if not expenses:
        print("\nNo expenses recorded yet to delete!")
        return

    view_expenses()

    while True:
        try:
            target_id = int(
                input("\nEnter the ID of the expense to delete: ")
            )
            break
        except ValueError:
            print("Enter a valid number.")

    target_expense = None
    for exp in expenses:
        if exp["id"] == target_id:
            target_expense = exp
            break

    if not target_expense:
        print(f"\nError: Expense with ID {target_id} not found!")
        return

    print(
        f"\nFound Expense: [ID: {target_expense['id']} | Date: {target_expense.get('date', 'N/A')} | {target_expense['description']} | PKR {target_expense['amount']}]"
    )
    confirm = (
        input("Are you sure you want to delete this expense? (y/n): ")
        .strip()
        .lower()
    )

    if confirm in ["y", "yes"]:
        expenses.remove(target_expense)
        print(f"\nExpense ID {target_id} deleted successfully!")
    else:
        print("\nDeletion cancelled. Expense was not removed.")


def export_to_csv():
    if not expenses:
        print("\nNo expenses available to export!")
        return

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_filename = f"expenses_export_{timestamp}.csv"

    try:
        with open(csv_filename, "w", newline="") as csvfile:
            fieldnames = [
                "ID",
                "Description",
                "Amount (PKR)",
                "Category",
                "Date/Time",
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for exp in expenses:
                writer.writerow(
                    {
                        "ID": exp["id"],
                        "Description": exp["description"],
                        "Amount (PKR)": exp["amount"],
                        "Category": exp["category"],
                        "Date/Time": exp.get("date", "N/A"),
                    }
                )

        print(
            f"\n✅ All expense records successfully exported to '{csv_filename}'!"
        )
    except Exception as err:
        print(f"\nError exporting to CSV: {err}")


# ==========================================
# File I/O Operations
# ==========================================
def save_expenses():
    try:
        with open(FILE_NAME, "w") as file:
            file.write(f"BUDGET:{monthly_budget}\n")
            for e in expenses:
                dt = e.get("date", "N/A")
                file.write(
                    f"{e['id']},{e['description']},{e['amount']},{e['category']},{dt}\n"
                )
        print(f"\nData successfully saved in '{FILE_NAME}'.")
    except Exception as err:
        print(f"\nError saving data: {err}")


def load_expenses():
    global expense_id, monthly_budget

    if not os.path.exists(FILE_NAME):
        return

    try:
        with open(FILE_NAME, "r") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue

                if line.startswith("BUDGET:"):
                    monthly_budget = float(line.split(":")[1])
                    continue

                parts = line.split(",")
                if len(parts) >= 4:
                    rec_id = int(parts[0])
                    rec_date = parts[4] if len(parts) >= 5 else "N/A"
                    rec = {
                        "id": rec_id,
                        "description": parts[1],
                        "amount": float(parts[2]),
                        "category": parts[3],
                        "date": rec_date,
                    }
                    expenses.append(rec)
                    if rec_id >= expense_id:
                        expense_id = rec_id + 1
    except Exception as err:
        print(f"\nWarning: Could not read existing file data ({err}).")


# ==========================================
# Main Method
# ==========================================
def main():
    load_expenses()
    while True:
        clear_screen()
        display_menu()
        choice = input("select option [1-10]: ").strip()
        print()

        match choice:
            case "1":
                add_expense()
            case "2":
                view_expenses()
            case "3":
                category_summary()
            case "4":
                filter_by_category()
            case "5":
                delete_expense()
            case "6":
                set_monthly_budget()
            case "7":
                export_to_csv()
            case "8":
                sort_expenses()
            case "9":
                save_expenses()
            case "10":
                save_expenses()
                print("Exiting......")
                break
            case _:
                print("Invalid Option! Please select from [1-10]")

        if choice != "10":
            input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()