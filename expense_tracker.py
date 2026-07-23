import csv
from datetime import datetime
import os
import shutil
import subprocess
from colorama import Fore, Style, init
from pyfiglet import Figlet

# expense_tracker.py
# CloudExify Python Internship — Month 1 Project 1
# Samiullah | Registration No: CX-INT-2026-PY-0057


init(autoreset=True)


# ==========================================
# Global Variables
# ==========================================
expenses = []
expense_id = 1
monthly_budget = 0.0 
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
        print(f"{Fore.CYAN}{Style.BRIGHT}{line.center(columns)}")


def display_menu():
    print_banner()
    print(f"{Fore.BLUE}{'=' * 50}")
    print(f"{Fore.GREEN}[1]. {Style.RESET_ALL}Add Expense")
    print(f"{Fore.GREEN}[2]. {Style.RESET_ALL}View Expenses")
    print(f"{Fore.GREEN}[3]. {Style.RESET_ALL}Category summary")
    print(f"{Fore.GREEN}[4]. {Style.RESET_ALL}Filter By Category")
    print(f"{Fore.GREEN}[5]. {Style.RESET_ALL}Delete Expense")
    print(f"{Fore.GREEN}[6]. {Style.RESET_ALL}Edit Expense")
    print(f"{Fore.GREEN}[7]. {Style.RESET_ALL}Set Monthly Budget")
    print(f"{Fore.GREEN}[8]. {Style.RESET_ALL}Export to CSV Format")
    print(f"{Fore.GREEN}[9]. {Style.RESET_ALL}Sort Expenses")
    print(f"{Fore.GREEN}[10]. {Style.RESET_ALL}Monthly Statistics")
    print(f"{Fore.GREEN}[11]. {Style.RESET_ALL}Save Expenses")
    print(f"{Fore.GREEN}[12]. {Style.RESET_ALL}Save and Exit")
    print(f"{Fore.BLUE}{'=' * 50}")

    
    if monthly_budget > 0:
        current_month = datetime.now().strftime("%Y-%m")
        current_month_spent = sum(
            exp["amount"]
            for exp in expenses
            if exp.get("date", "").startswith(current_month)
        )

        print(
            f"{Fore.MAGENTA}Monthly Budget Target: PKR {monthly_budget:,.2f} | Spent: PKR {current_month_spent:,.2f}"
        )

        if current_month_spent > monthly_budget:
            excess = current_month_spent - monthly_budget
            print(f"{Fore.RED}{'=' * 50}")
            print(
                f"{Fore.RED}{Style.BRIGHT}WARNING: You have EXCEEDED your monthly budget by PKR {excess:,.2f}!"
            )
            print(f"{Fore.RED}{'=' * 50}")


# ==========================================
# Core Logic Functions
# ==========================================


def set_monthly_budget():
    global monthly_budget
    print(f"\n{Fore.CYAN}{Style.BRIGHT}--- SET MONTHLY BUDGET ---")
    print(f"Current Target: PKR {monthly_budget:,.2f}")

    while True:
        try:
            val = float(
                input("Enter new monthly budget target (PKR) [0 to disable]: ")
            )
            if val < 0:
                print(f"{Fore.RED}Budget target cannot be negative!")
                continue
            monthly_budget = val
            print(
                f"\n{Fore.GREEN}Monthly budget target successfully set to PKR {monthly_budget:,.2f}!"
            )
            break
        except ValueError:
            print(f"{Fore.RED}Please enter a valid number.")


def add_expense():
    global expense_id

    print(f"\n{Fore.CYAN}{Style.BRIGHT}--- ADD NEW EXPENSE ---")

    description = input("Description: ").strip()
    while not description:
        print(f"{Fore.RED}Description can't be empty!")
        description = input("Description: ").strip()

    while True:
        try:
            amount = float(input("Amount: "))
            if amount <= 0:
                print(f"{Fore.RED}Amount can't be zero or negative!")
                continue
            break
        except ValueError:
            print(f"{Fore.RED}Please enter a valid number")

    categories = ["Food", "Transport", "Shopping", "Bills", "Other"]
    print(f"\n{Fore.YELLOW}Categories:")
    for index, category_name in enumerate(categories, 1):
        print(f"  {index}). {category_name}")

    while True:
        try:
            choice = int(input("Select category (1-5): "))
            if 1 <= choice <= len(categories):
                category = categories[choice - 1]
                break
            print(f"{Fore.RED}Select from [1-5]!")
        except ValueError:
            print(f"{Fore.RED}Enter a valid number!")

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
        f"\n{Fore.GREEN}✅ Expense added successfully at {current_time}! Assigned ID: #{expense_id}"
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
                f"\n{Fore.RED}{Style.BRIGHT}⚠️  ALERT: This expense puts you OVER your monthly budget of PKR {monthly_budget:,.2f}!"
            )

    expense_id += 1


def edit_expense():
    if not expenses:
        print(f"\n{Fore.YELLOW}No expenses recorded yet to edit!")
        return

    view_expenses()

    while True:
        try:
            target_id = int(
                input("\nEnter the ID of the expense to edit: ")
            )
            break
        except ValueError:
            print(f"{Fore.RED}Enter a valid number.")

    target_expense = None
    for exp in expenses:
        if exp["id"] == target_id:
            target_expense = exp
            break

    if not target_expense:
        print(f"\n{Fore.RED}Error: Expense with ID {target_id} not found!")
        return

    print(f"\n{Fore.CYAN}{Style.BRIGHT}--- EDIT EXPENSE ---")
    print(f"{Style.DIM}(Press Enter without typing to keep the existing value)")

    # 1. New Description
    new_desc = input(
        f"Description [{target_expense['description']}]: "
    ).strip()
    if new_desc:
        target_expense["description"] = new_desc

    # 2. New Amount
    while True:
        amt_str = input(
            f"Amount PKR [{target_expense['amount']}]: "
        ).strip()
        if not amt_str:
            break
        try:
            new_amt = float(amt_str)
            if new_amt <= 0:
                print(f"{Fore.RED}Amount must be greater than zero!")
                continue
            target_expense["amount"] = new_amt
            break
        except ValueError:
            print(f"{Fore.RED}Please enter a valid number.")

    # 3. New Category
    categories = ["Food", "Transport", "Shopping", "Bills", "Other"]
    print(f"\nCurrent Category: {target_expense['category']}")
    print(f"{Fore.YELLOW}Select New Category (or press Enter to keep current):")
    for index, category_name in enumerate(categories, 1):
        print(f"  {index}). {category_name}")

    cat_choice = input("Choice (1-5): ").strip()
    if cat_choice:
        try:
            c_int = int(cat_choice)
            if 1 <= c_int <= len(categories):
                target_expense["category"] = categories[c_int - 1]
        except ValueError:
            print(f"{Fore.YELLOW}Invalid category selection. Keeping current category.")

    print(f"\n{Fore.GREEN}✅ Expense ID #{target_id} successfully updated!")


def view_expenses(custom_list=None, title="ALL EXPENSES"):
    data_to_show = custom_list if custom_list is not None else expenses

    if not data_to_show:
        print(f"\n{Fore.YELLOW}No Expenses to display!")
        return

    print(f"\n{Fore.BLUE}" + "=" * 70)
    print(f"{Fore.CYAN}{Style.BRIGHT}                --- {title} ---                ")
    print(f"{Fore.BLUE}" + "=" * 70)

    print(
        f"{Fore.MAGENTA}{Style.BRIGHT}{'ID':<5} {'Date/Time':<18} {'Description':<18} {'Category':<10} {'Amount (PKR)':>12}"
    )
    print(f"{Fore.BLUE}" + "-" * 70)

    total_amount = 0.0

    for exp in data_to_show:
        dt = exp.get("date", "N/A")
        print(
            f"#{exp['id']:<4} {dt:<18} {exp['description']:<18} {exp['category']:<10} {Fore.GREEN}{exp['amount']:>12.2f}"
        )
        total_amount += exp["amount"]

    print(f"{Fore.BLUE}" + "-" * 70)
    print(f"{Style.BRIGHT}{'TOTAL EXPENSE:':<55} {Fore.GREEN}{Style.BRIGHT}PKR {total_amount:>9.2f}")
    print(f"{Fore.BLUE}" + "=" * 70)


def category_summary():

    if not expenses:
        print(f"\n{Fore.YELLOW}No Expenses for now!")
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

    print(f"\n{Fore.BLUE}" + "=" * 45)
    print(f"{Fore.CYAN}{Style.BRIGHT}            --- CATEGORY SUMMARY ---         ")
    print(f"{Fore.BLUE}" + "=" * 45)
    print(f"{Fore.MAGENTA}{Style.BRIGHT}{'Category':<15} {'Amount (PKR)':>12} {'Percentage':>12}")
    print(f"{Fore.BLUE}" + "-" * 45)

    for category_name, cat_total in summary.items():
        percentage = (cat_total / grand_total) * 100
        print(
            f"{category_name:<15} "
            f"{Fore.GREEN}{cat_total:>12.2f}{Style.RESET_ALL} "
            f"{Fore.YELLOW}{percentage:>11.1f}%"
        )

    print(f"{Fore.BLUE}" + "-" * 45)
    print(f"{Style.BRIGHT}{'GRAND TOTAL:':<15} {Fore.GREEN}{Style.BRIGHT}PKR {grand_total:>8.2f}  (100.0%)")
    print(f"{Fore.BLUE}" + "=" * 45)


def filter_by_category():

    if not expenses:
        print(f"\n{Fore.YELLOW}No expenses recorded yet to filter!")
        return

    categories = ["Food", "Transport", "Shopping", "Bills", "Other"]
    print(f"\n{Fore.YELLOW}Select Category to Filter:")
    for index, category_name in enumerate(categories, 1):
        print(f"  {index}). {category_name}")

    while True:
        try:
            choice = int(input("Select category (1-5): "))
            if 1 <= choice <= len(categories):
                selected_category = categories[choice - 1]
                break
            print(f"{Fore.RED}Please select a number from 1 to 5!")
        except ValueError:
            print(f"{Fore.RED}Please enter a valid number.")

    filtered_expenses = [
        exp for exp in expenses if exp["category"] == selected_category
    ]

    if not filtered_expenses:
        print(f"\n{Fore.YELLOW}No expenses found under '{selected_category}' category.")
        return

    view_expenses(
        filtered_expenses, title=f"EXPENSES FOR: {selected_category.upper()}"
    )


def sort_expenses():
    if not expenses:
        print(f"\n{Fore.YELLOW}No expenses recorded yet to sort!")
        return

    print(f"\n{Fore.CYAN}{Style.BRIGHT}--- SORT EXPENSES ---")
    print("[1]. Sort by Amount (Low to High)")
    print("[2]. Sort by Amount (High to Low)")
    print("[3]. Sort by Date (Oldest First)")
    print("[4]. Sort by Date (Newest First)")

    while True:
        choice = input("Select sort option [1-4]: ").strip()
        if choice in ["1", "2", "3", "4"]:
            break
        print(f"{Fore.RED}Invalid choice! Select from [1-4].")

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


def monthly_statistics():
    if not expenses:
        print(f"\n{Fore.YELLOW}No expenses recorded yet to calculate monthly stats!")
        return

    monthly_data = {}

    for exp in expenses:
        date_str = exp.get("date", "")
        # Extract YYYY-MM prefix from timestamp
        month_key = date_str[:7] if len(date_str) >= 7 else "Unknown"

        if month_key not in monthly_data:
            monthly_data[month_key] = {"total": 0.0, "count": 0}

        monthly_data[month_key]["total"] += exp["amount"]
        monthly_data[month_key]["count"] += 1

    # Sort months chronologically
    sorted_months = sorted(monthly_data.keys())

    # Find highest and lowest spending months
    highest_month = max(monthly_data.items(), key=lambda x: x[1]["total"])
    lowest_month = min(monthly_data.items(), key=lambda x: x[1]["total"])

    print(f"\n{Fore.BLUE}" + "=" * 60)
    print(f"{Fore.CYAN}{Style.BRIGHT}              --- MONTHLY STATISTICS ---              ")
    print(f"{Fore.BLUE}" + "=" * 60)

    print(
        f"{Fore.MAGENTA}{Style.BRIGHT}{'Month':<12} {'Total Spent (PKR)':>18} {'Tx Count':>12} {'Avg/Tx (PKR)':>15}"
    )
    print(f"{Fore.BLUE}" + "-" * 60)

    for m in sorted_months:
        tot = monthly_data[m]["total"]
        cnt = monthly_data[m]["count"]
        avg = tot / cnt if cnt > 0 else 0.0

        # Highlight highest month with RED indicator, others with GREEN
        is_highest = (m == highest_month[0] and len(sorted_months) > 1)
        color = Fore.RED if is_highest else Fore.GREEN

        m_display = f"{m} 🔥" if is_highest else m
        print(
            f"{m_display:<12} {color}{tot:>18.2f}{Style.RESET_ALL} {cnt:>12} {avg:>15.2f}"
        )

    print(f"{Fore.BLUE}" + "=" * 60)
    
    # Key Highlights Box
    print(f"\n{Fore.CYAN}{Style.BRIGHT}📊 KEY HIGHLIGHTS:")
    print(
        f"  🔥 {Style.BRIGHT}Highest Spending Month: {Fore.RED}{highest_month[0]}{Style.RESET_ALL} "
        f"(PKR {highest_month[1]['total']:,.2f} across {highest_month[1]['count']} transactions)"
    )
    print(
        f"  💡 {Style.BRIGHT}Lowest Spending Month : {Fore.GREEN}{lowest_month[0]}{Style.RESET_ALL} "
        f"(PKR {lowest_month[1]['total']:,.2f} across {lowest_month[1]['count']} transactions)"
    )
    print(f"{Fore.BLUE}" + "=" * 60)


def delete_expense():

    if not expenses:
        print(f"\n{Fore.YELLOW}No expenses recorded yet to delete!")
        return

    view_expenses()

    while True:
        try:
            target_id = int(
                input("\nEnter the ID of the expense to delete: ")
            )
            break
        except ValueError:
            print(f"{Fore.RED}Enter a valid number.")

    target_expense = None
    for exp in expenses:
        if exp["id"] == target_id:
            target_expense = exp
            break

    if not target_expense:
        print(f"\n{Fore.RED}Error: Expense with ID {target_id} not found!")
        return

    print(
        f"\n{Fore.YELLOW}Found Expense: [ID: #{target_expense['id']} | Date: {target_expense.get('date', 'N/A')} | {target_expense['description']} | PKR {target_expense['amount']}]"
    )
    confirm = (
        input(f"{Fore.RED}Are you sure you want to delete this expense? (y/n): ")
        .strip()
        .lower()
    )

    if confirm in ["y", "yes"]:
        expenses.remove(target_expense)
        print(f"\n{Fore.GREEN}✅ Expense ID #{target_id} deleted successfully!")
    else:
        print(f"\n{Fore.YELLOW}Deletion cancelled. Expense was not removed.")


def export_to_csv():
    if not expenses:
        print(f"\n{Fore.YELLOW}No expenses available to export!")
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
            f"\n{Fore.GREEN}✅ All expense records successfully exported to '{csv_filename}'!"
        )
    except Exception as err:
        print(f"\n{Fore.RED}Error exporting to CSV: {err}")


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
        print(f"\n{Fore.GREEN}✅ Data successfully saved in '{FILE_NAME}'.")
    except Exception as err:
        print(f"\n{Fore.RED}Error saving data: {err}")


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
        print(f"\n{Fore.YELLOW}Warning: Could not read existing file data ({err}).")


# ==========================================
# Main Method
# ==========================================
def main():
    load_expenses()
    while True:
        clear_screen()
        display_menu()
        choice = input(f"{Fore.CYAN}Select option [1-12]: {Style.RESET_ALL}").strip()
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
                edit_expense()
            case "7":
                set_monthly_budget()
            case "8":
                export_to_csv()
            case "9":
                sort_expenses()
            case "10":
                monthly_statistics()
            case "11":
                save_expenses()
            case "12":
                save_expenses()
                print(f"{Fore.CYAN}Exiting......")
                break
            case _:
                print(f"{Fore.RED}Invalid Option! Please select from [1-12]")

        if choice != "12":
            input(f"\n{Style.DIM}Press Enter to continue...")


if __name__ == "__main__":
    main()