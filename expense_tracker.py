# Import the Expense class from the expense module.
from expense import Expense

# Import the calendar and datetime modules for date-related calculations.
import calendar
import datetime

# Define the main function to run the Expense Tracker.
def main():
    print(f"🎯 Running Expense Tracker!")

    # Specify the file path where expense data will be stored.
    expense_file_path = "expenses.csv"

    # Set the budget for expenses.
    budget = 2000

    # Get user input for a new expense.
    expense = get_user_expense()

    # Save the user's expense to the specified file.
    save_expense_to_file(expense, expense_file_path)

    # Read and summarize expenses from the file.
    summarize_expenses(expense_file_path, budget)

# Function to get user input for a new expense.
def get_user_expense():
    print(f"🎯 Getting User Expense")

    # Prompt the user to enter expense details.
    expense_name = input("Enter expense name: ")
    expense_amount = float(input("Enter expense amount: "))

    # Define expense categories.
    expense_categories = [
        "🍔 Food",
        "🏠 Home",
        "💼 Work",
        "🎉 Fun",
        "✨ Misc",
    ]

    while True:
        # Display available categories and allow the user to select one.
        print("Select a category: ")
        for i, category_name in enumerate(expense_categories):
            print(f"  {i + 1}. {category_name}")

        value_range = f"[1 - {len(expense_categories)}]"
        selected_index = int(input(f"Enter a category number {value_range}: ")) - 1

        if selected_index in range(len(expense_categories)):
            selected_category = expense_categories[selected_index]

            # Create a new Expense object and return it.
            new_expense = Expense(
                name=expense_name, category=selected_category, amount=expense_amount
            )
            return new_expense
        else:
            print("Invalid category. Please try again!")

# Function to save an expense to a file.
def save_expense_to_file(expense: Expense, expense_file_path):
    print(f"🎯 Saving User Expense: {expense} to {expense_file_path}")
    with open(expense_file_path, "a") as f:
        f.write(f"{expense.name},{expense.amount},{expense.category}\n")

# Function to read and summarize expenses from a file.
def summarize_expenses(expense_file_path, budget):
    print(f"🎯 Summarizing User Expense")
    expenses: list[Expense] = []

    # Read expense data from the file and create Expense objects.
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

    # Calculate and display expenses by category.
    amount_by_category = {}
    for expense in expenses:
        key = expense.category
        if key in amount_by_category:
            amount_by_category[key] += expense.amount
        else:
            amount_by_category[key] = expense.amount

    print("Expenses By Category 📈:")
    for key, amount in amount_by_category.items():
        print(f"  {key}: ${amount:.2f}")

    # Calculate and display total spent, remaining budget, and daily budget.
    total_spent = sum([x.amount for x in expenses])
    print(f"💵 Total Spent: ${total_spent:.2f}")

    remaining_budget = budget - total_spent
    print(f"✅ Budget Remaining: ${remaining_budget:.2f}")

    now = datetime.datetime.now()
    days_in_month = calendar.monthrange(now.year, now.month)[1]
    remaining_days = days_in_month - now.day

    daily_budget = remaining_budget / remaining_days
    print(green(f"👉 Budget Per Day: ${daily_budget:.2f}"))

# Function to add green color to text for console output.
def green(text):
    return f"\033[92m{text}\033[0m"

# Check if the script is executed as the main program.
if __name__ == "__main__":
    main()