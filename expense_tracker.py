from pyfiglet import Figlet
import shutil
import sys


# def clear_screen():
#     sys.stdout.write("\033[H\033[2J")
#     sys.stdout.flush()

def print_banner():
    columns = shutil.get_terminal_size().columns
    f=Figlet(font='small')
    banner=f.renderText('Expense Tracker')
    for line in banner.splitlines():
        print(line.center(columns))

def display_menu():
    print("="*40)
    print('[1]. Add Expense')
    print('[2]. View Expenses')
    print('[3]. Category summary')
    print('[4]. Filter By Category')
    print('[5]. Delete Expense')
    print('[6]. Save Expenses')
    print('[7]. Save and Exit')
    print("="*40)



def main():
    print_banner()
    while True:
        #clear_screen()
        display_menu()
        choice=input('select option [1-7]: ').strip()
        print()
        match choice:
            case '1':
                print("Add expense called \n")
            case '2':
                print("view expense called")
            case '3':
                print("category summary called")
            case '4':
                print("filter by category called")
            case '5':
                print("delete expense called")
            case '6':
                print("save expense called")
            case '7':
                print("Exiting......")
                break
            case _:
                print("Invalid Option! Please select from [1-7]")

if __name__ == "__main__":
    main()