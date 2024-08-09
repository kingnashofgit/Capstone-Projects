# Importing sqlite3 database
import sqlite3

#  Connect to SQLite database 
conn = sqlite3.connect ('tracker_app.db')
cursor = conn.cursor()

# Creating tables
def create_tables():
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS expenses (id INTEGER PRIMARY KEY AUTOINCREMENT,
               expense_name TEXT NOT NULL UNIQUE,
               expense_category TEXT NOT NULL,
               amount REAL NOT NULL
                )
            ''')
    
    cursor.execute('''
               CREATE TABLE IF NOT EXISTS income (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               income_name TEXT NOT NULL UNIQUE,
               income_amount REAL NOT NULL,
               income_category TEXT NOT NULL
            )
        ''')

    cursor.execute('''
               CREATE TABLE IF NOT EXISTS budget (
               budget_category TEXT NOT NULL UNIQUE,
               budget_amount REAL NOT NULL,
               
               FOREIGN KEY (budget_category) REFERENCES expense_category
            )
        ''')
    
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS goals (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               current_amount REAL NOT NULL,
               target_amount  REAL NOT NULL
            )
        ''')

create_tables()
conn.commit()


# To handle user input for adding expenses
def add_expense(expense_name,expense_category,amount):
    cursor.execute('INSERT INTO expenses (expense_name, expense_category, amount) VALUES (?,?, ?)', 
                (expense_name,expense_category,amount))
    conn.commit()


# To handle user input for viewing expenses
def view_expenses():
    cursor.execute('SELECT * FROM expenses')
    return cursor.fetchall()


# To handle user input for viewing expenses by category
def view_expense_category():
    cursor.execute('SELECT expense_category FROM expenses')
    return cursor.fetchall()


# To handle user input for adding income
def add_income(income_name,income_amount,income_category):
    cursor.execute('INSERT INTO income (income_name,income_amount, income_category) VALUES (?,?,?)',
                (income_name,income_amount,income_category))
    conn.commit()


def view_income():# To handle user input for viewing income
    cursor.execute('SELECT * FROM income')
    return cursor.fetchall()


# To handle user input for viewing income by category
def view_income_category():
    cursor.execute('SELECT income_category FROM income')
    return cursor.fetchall()


# To handle user input for adding a budget
def add_budget (budget_category,budget_amount):
    cursor.execute('INSERT  OR IGNORE INTO budget (budget_category, budget_amount) VALUES (?,?)',
                (budget_category,budget_amount))
    conn.commit()


# To handle user input for viewing budget by category
def view_budget_category():
    cursor.execute('SELECT budget_category,budget_amount FROM budget')
    return cursor.fetchall()


# Getting the sum of the budget_amount
def get_total_budget(): 
    cursor.execute('SELECT SUM(budget_amount) FROM budget')
    total_budget = cursor.fetchone()[0]
    if total_budget:
        return total_budget
    else:
        return 0 
    
      
# Getting the sum of income_amount
def get_total_income(): 
    cursor.execute('SELECT SUM(income_amount) FROM income ') 
    total_income = cursor.fetchone()[0]
    if total_income:
        return total_income
    else:
        return 0
    
    
# Checking the total budget by adding total budget and budget amountS   
def check_total_budget(budget_category,budget_amount):
    total_income = get_total_income()
    total_budget = get_total_budget()
    if total_budget + budget_amount > total_income:
        print("Budget exceeds income, enter amount again.")
    else:
        add_budget(budget_category,budget_amount)
        print("Budget successfuly added.")


# Getting the sum of all the amounts in the expenses table
def get_total_expenses(): 
    cursor.execute('SELECT SUM(amount) FROM expenses ')
    total_expenses = cursor.fetchone()[0]
    if total_expenses:
        return total_expenses
    else:
        return 0
    
    
# Checking the total expenses by adding total expenses and expense amount
def check_total_expenses(expense_name,expense_category,amount):
    total_expenses = get_total_expenses()
    total_budget = get_total_budget()
    if total_expenses + amount > total_budget:
        print("Budget has been exceeded, enter amount again.")
    else:
        add_expense(expense_name,expense_category,amount)
        print("Expense successfuly added.")


# To handle user input for adding financial goals
def add_goals(current_amount,target_amount):
    cursor.execute ('SELECT id FROM goals')
    existing_goal = cursor.fetchone()
    if existing_goal:
        cursor.execute('''UPDATE goals SET current_amount =?,target_amount=? 
        WHERE id=?''',(current_amount,target_amount,existing_goal[0]))
    else:
        cursor.execute('''INSERT INTO goals (current_amount,target_amount) 
         VALUES (?,?)''', (current_amount,target_amount))
    conn.commit()


# To get the sum of the savings amounts from the expense table
def get_total_savings():
    cursor.execute('''SELECT SUM(amount) FROM expenses WHERE expense_category = 'savings';''')
    total_savings = cursor.fetchone()[0]
    if total_savings:
        return total_savings
    else:
        return 0
    

# To check the total savings of the user   
def check_total_savings(current_amount,target_amount):
    total_savings = get_total_savings()
    if current_amount + total_savings > target_amount:
        print("Financial goal achieved.")
    else:
        savings_left =target_amount - (current_amount + total_savings)
        print(f"You have {savings_left} left to save.")


# To handle user input for viewing financial goals
def view_goals():
    cursor.execute('SELECT current_amount,target_amount FROM goals')
    goals = cursor.fetchone()
    current_amount = goals[0]
    target_amount = goals[1]
    check_total_savings(current_amount,target_amount)


#  The menu for user interaction
def main_menu():
    while True:
        print("\nBudget Tracker Menu")
        print("1. Add expense")
        print("2. View expenses")
        print("3. View expenses by category")
        print("4. Add income")
        print("5. View income")
        print("6. View income by category")
        print("7. Set budget for a category")
        print("8. View budget for a category")
        print("9. Set financial goals")
        print("10. View progress towards financial goals")
        print("11. Quit")

        choice = input("Select an option: ")

        if choice == '1':# For the user to add an expense
            print("ADDING EXPENSES.")
            expense_name = input("Enter the expense name.")
            expense_category = input("Enter expense category.")
            amount = float(input("Enter expense amount."))
            check_total_expenses(expense_name,expense_category,amount)

        
        elif choice == '2':# For the user to add an expense
            print("VIEWING EXPENSES.")
            expenses = view_expenses()
            for expense in expenses:
                print(f"Expense name: {expense[1]} Expense category: .\
                {expense[2]} Expense amount: {expense[3]}")
                # using f-string to give more accurate information to the user


        elif choice == '3': # For the user to view expenses by category
            print("VIEWING EXPENSES BY CATEGORY.")
            expenses = view_expense_category()
            for exp in expenses:
                print(f"Expenses by category: {exp[0]}") 
                # f-string to be more descriptive


        elif choice == '4':# For the user to add an income
            print("ADDING INCOME.")
            income_name = input("Enter income name.")
            income_amount = float(input("Enter income amount."))
            income_category = input("Enter income category name.")
            add_income(income_name,income_amount,income_category)


        elif choice ==  '5':# For the user to view income
            print("VIEWING INCOME.")
            income = view_income()
            for inc in income:
                print(f"Income name: {inc[1]} Income amount: {inc[2]} Income .\
                      category:{inc[3]}")
                

        elif choice == '6': # For the user to view income by category
            print("VIEWING INCOME BY CATEGORY.")
            income = view_income_category()
            for inc in income:
                print(f"income by category: {inc[0]}")


        elif choice == '7':  # Code for setting a budget for a category
            print("SETTING A BUDGET FOR A CATEGORY.")
            budget_category = input("Enter budget category.")
            budget_amount = float(input("Enter budget amount."))
            check_total_budget(budget_category,budget_amount)


        elif choice == '8':  # Code for viewing budget for a category
            print("VIEWING A BUDGET FOR A CATEGORY.")
            budget = view_budget_category()
            for budg in budget:
                print(f"Budget category: {budg[0]} Budget amount: {budg[1]}")
                # Using f-string to be more accurate


        elif choice == '9': # Code for setting financial goals
            print("SETTING FINANCIAL GOALS.")
            current_amount = float(input("Enter current amount."))
            target_amount = float(input("Enter target amount."))
            add_goals(current_amount,target_amount)


        elif choice =='10': # Code for viewing progress towards financial goals
            print("VIEWING PROGRESS TOWARDS FINANCIAL GOALS.")
            view_goals()


        elif choice == '11':
            print("Exiting the program.")
            break

        else:
            print("Invalid choice. Please try again.")


main_menu()

# Close the connection to the database
conn.close()





