from pyfiglet import Figlet
import shutil
import os
import subprocess

# expense_tracker.py
# CloudExify Python Internship — Month 1 Project 1
# Samiullah | Registration No: CX-INT-2026-PY-0057

expenses = []
expense_id = 1


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
    print("=" * 40)
    print("[1]. Add Expense")
    print("[2]. View Expenses")
    print("[3]. Category summary")
    print("[4]. Filter By Category")
    print("[5]. Delete Expense")
    print("[6]. Save Expenses")
    print("[7]. Save and Exit")
    print("=" * 40)


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

    expense = {
        "id": expense_id,
        "description": description,
        "amount": amount,
        "category": category,
    }

    expenses.append(expense)
    print(f"\nExpense added successfully! Assigned ID: {expense_id}")

    expense_id += 1


def view_expenses():
    
    if not expenses:
        print("\nNo Expenses for now!")
        return

    print("\n" + "=" * 52)
    print("                --- ALL EXPENSES ---                ")
    print("=" * 52)


    print(
        f"{'ID':<5} {'Description':<20} {'Category':<12} {'Amount (PKR)':>12}"
    )
    print("-" * 52)

    total_amount = 0.0

    
    for exp in expenses:
        print(
            f"{exp['id']:<5} "
            f"{exp['description']:<20} "
            f"{exp['category']:<12} "
            f"{exp['amount']:>12.2f}"
        )
        total_amount += exp["amount"]

    
    print("-" * 52)
    print(f"{'TOTAL EXPENSE:':<38} PKR {total_amount:>9.2f}")
    print("=" * 52)



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

    
    print("\n" + "=" * 52)
    print(
        f"          --- EXPENSES FOR: {selected_category.upper()} ---          "
    )
    print("=" * 52)
    print(
        f"{'ID':<5} {'Description':<20} {'Category':<12} {'Amount (PKR)':>12}"
    )
    print("-" * 52)

    category_total = 0.0
    for exp in filtered_expenses:
        print(
            f"{exp['id']:<5} "
            f"{exp['description']:<20} "
            f"{exp['category']:<12} "
            f"{exp['amount']:>12.2f}"
        )
        category_total += exp["amount"]

    print("-" * 52)
    print(
        f"{f'TOTAL FOR {selected_category.upper()}:':<38} PKR {category_total:>9.2f}"
    )
    print("=" * 52)


def main():
    while True:
        clear_screen()
        display_menu()
        choice = input("select option [1-7]: ").strip()
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
                print("delete expense called")
            case "6":
                print("save expense called")
            case "7":
                print("Exiting......")
                break
            case _:
                print("Invalid Option! Please select from [1-7]")

        if choice != "7":
            input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()