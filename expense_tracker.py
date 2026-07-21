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
    print_banner()  # Banner menu ke sath hi display hoga
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
                print("view expense called")
            case "3":
                print("category summary called")
            case "4":
                print("filter by category called")
            case "5":
                print("delete expense called")
            case "6":
                print("save expense called")
            case "7":
                print("Exiting......")
                break
            case _:
                print("Invalid Option! Please select from [1-7]")

        # Iss Pause se user output dekh sakega, warna screen foran clear ho jati hai
        if choice != "7":
            input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()