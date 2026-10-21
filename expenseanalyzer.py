# Python Expense Analyzer
import json
import os

DATA_FILE = "expenselist.json"


def get_text(prompt):
    """Get non-empty text input from the user."""
    while True:
        value = input(prompt).strip()

        if value:
            return value

        print("This field cannot be empty.")


def get_amount():
    """Get a valid, non-negative expense amount from the user."""
    while True:
        try:
            amount = float(input("Please enter expense amount: $"))

            if amount < 0:
                print("Expense amount cannot be negative.")
                continue

            return amount

        except ValueError:
            print("Please enter a numerical value.")


def load_expenses():
    """Load expenses from the JSON file."""
    if not os.path.exists(DATA_FILE):
        return []

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            expenses = json.load(file)

        if not isinstance(expenses, list):
            print(f"Invalid data format in {DATA_FILE}.")
            print("Starting with an empty expense list.")
            return []

        return expenses

    except (OSError, json.JSONDecodeError) as error:
        print(f"Could not read {DATA_FILE}: {error}")
        print("Starting with an empty expense list.")
        return []


def save_expenses(expenses):
    """Save expenses to the JSON file."""
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(expenses, file, indent=4)

        return True

    except OSError as error:
        print(f"Could not save expenses: {error}")
        return False


def add_expense(expenses):
    """Add a new expense and save it to the JSON file."""
    expense = {
        "name": get_text("Enter expense name: "),
        "category": get_text("Enter category name: "),
        "amount": get_amount(),
    }

    expenses.append(expense)

    if save_expenses(expenses):
        print("Expense added and saved.")
    else:
        expenses.pop()
        print("Expense was not added because it could not be saved.")


def view_expenses(expenses):
    """Display all recorded expenses."""
    if not expenses:
        print("No expenses recorded yet.")
        return

    print("\n---- Expenses ----")
    print(f"{'Name':<25} {'Category':<20} {'Amount':>12}")
    print("-" * 60)

    for expense in expenses:
        print(
            f"{expense['name']:<25} "
            f"{expense['category']:<20} "
            f"${expense['amount']:>11.2f}"
        )


def generate_report(expenses):
    """Generate a summary of total expenses by category."""
    if not expenses:
        print("No expenses available to report.")
        return

    total = sum(expense["amount"] for expense in expenses)

    category_totals = {}

    for expense in expenses:
        category = expense["category"]

        category_totals[category] = (
            category_totals.get(category, 0) + expense["amount"]
        )

    print("\n---- Expense Report ----")
    print(f"Number of expenses: {len(expenses)}")
    print(f"Total expenses:     ${total:.2f}")

    print("\nTotals by category:")

    for category, amount in sorted(category_totals.items()):
        print(f"   {category}: ${amount:.2f}")


def main():
    """Run the Business Expense Analyzer."""
    expenses = load_expenses()

    while True:
        print("\n---- Business Expense Analyzer ----")
        print("1. Add expense")
        print("2. View expenses")
        print("3. Generate report")
        print("4. Exit")

        user_choice = input("Choose an option: ").strip()

        if user_choice == "1":
            add_expense(expenses)

        elif user_choice == "2":
            view_expenses(expenses)

        elif user_choice == "3":
            generate_report(expenses)

        elif user_choice == "4":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Select a number from 1 to 4.")


if __name__ == "__main__":
    main()

