# Import necessary modules
from expense import Expense
import calendar
import datetime

# Define the main function
def main():
    # Display a welcome message
    print(f"🎯 Running Expense Tracker!")

    # Specify the file path to store expense data
    expense_file_path = "expenses.csv"

    # Get the initial budget from the user
    budget = get_initial_budget()

    while True:
        # Get user input for expense.
        expense = get_user_expense()

        # Write their expense to a file.
        save_expense_to_file(expense, expense_file_path)

        # Ask the user if they want to add another expense.
        another_expense = input("Add another expense? (yes/no): ").strip().lower()

        if another_expense != "yes":
            break  # Exit the loop if the user's response is not "yes"

    # Read the file and summarize expenses
    summarize_expenses(expense_file_path, budget)

# Function to get and validate the user's initial budget
def get_initial_budget():
    print(f"🎯 Getting Initial Budget")
    while True:
        try:
            initial_budget = float(input("Enter your budget: $"))
            if initial_budget >= 0:
                return initial_budget
            else:
                print("Budget must be a positive number. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a valid numeric value for your budget.")

# Function to get user input for a new expense
def get_user_expense():
    print(f"🎯 Getting User Expense")
    expense_name = input("Enter expense name: ")
    expense_amount = float(input("Enter expense amount: "))
    expense_categories = [
        "🍔 Food",
        "🏠 Home",
        "💼 Work",
        "🎉 Fun",
        "✨ Misc",
    ]

    while True:
        print("Select a category: ")
        for i, category_name in enumerate(expense_categories):
            print(f"  {i + 1}. {category_name}")

        value_range = f"[1 - {len(expense_categories)}]"
        selected_index = int(input(f"Enter a category number {value_range}: ")) - 1

        if selected_index in range(len(expense_categories)):
            selected_category = expense_categories[selected_index]
            new_expense = Expense(
                name=expense_name, category=selected_category, amount=expense_amount
            )
            return new_expense
        else:
            print("Invalid category. Please try again!")

# Function to save an expense to a file
def save_expense_to_file(expense: Expense, expense_file_path):
    print(f"🎯 Saving User Expense: {expense} to {expense_file_path}")
    with open(expense_file_path, "a") as f:
        f.write(f"{expense.name},{expense.amount},{expense.category}\n")

# Function to summarize expenses and display the results
def summarize_expenses(expense_file_path, budget):
    print(f"🎯 Summarizing User Expense")
    expenses: list[Expense] = []
    with open(expense_file_path, "r") as f:
        lines = f.readlines()
        for line in lines:
            expense_name, expense_amount, expense_category = line.strip().split(",")
            line_expense = Expense(
                name=expense_name,
                amount=float(expense_amount),
                category=expense_category,
            )
            expenses.append(line_expense)

    # Calculate expenses by category
    amount_by_category = {}
    for expense in expenses:
        key = expense.category
        if key in amount_by_category:
            amount_by_category[key] += expense.amount
        else:
            amount_by_category[key] = expense.amount

    # Display expenses by category
    print("Expenses By Category 📈:")
    for key, amount in amount_by_category.items():
        print(f"  {key}: ${amount:.2f}")

    # Calculate total spent
    total_spent = sum([x.amount for x in expenses])
    print(f"💵 Total Spent: ${total_spent:.2f}")

    # Calculate remaining budget
    remaining_budget = budget - total_spent
    print(f"✅ Budget Remaining: ${remaining_budget:.2f}")

    # Calculate daily budget
    now = datetime.datetime.now()
    days_in_month = calendar.monthrange(now.year, now.month)[1]
    remaining_days = days_in_month - now.day
    daily_budget = remaining_budget / remaining_days
    print(green(f"👉 Budget Per Day: ${daily_budget:.2f}"))

# Function to add green color to text for console output
def green(text):
    return f"\033[92m{text}\033[0m"

# Check if the script is executed as the main program
if __name__ == "__main__":
    main()

