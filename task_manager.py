import datetime


def login():
    while True:
        username = input("Enter your username: ")
        password = input("Enter your password: ")

        if validate_user(username, password):
            return username
        else:
            print("Invalid username or password. Please try again.")


def validate_user(username, password):
    with open("user.txt", "r") as file:
        for line in file:
            stored_username, stored_password = line.strip().split(", ")
            if username == stored_username and password == stored_password:
                return True
    return False


def register_user():
    new_username = input("Enter a new username: ")
    new_password = input("Enter a new password: ")
    confirm_password = input("Confirm the password: ")

    if new_password == confirm_password:
        with open("user.txt", "a") as file:
            # Space placed infront so that new registered user is added on a new line.
            file.write(f"\n{new_username}, {new_password}")
        print("User registered successfully!")
    else:
        print("Password confirmation does not match. User registration failed.")


# Add a task to a specific user.
def add_task():
    assigned_user = input("Enter the username of the person the task is assigned to: ")
    task_title = input("Enter the title of the task: ")
    task_description = input("Enter a description of the task: ")
    due_date = input("Enter the due date of the task (YYYY-MM-DD): ")
    current_date = datetime.date.today().strftime("%Y-%m-%d")
    completed = "No"

    with open("tasks.txt", "a") as file:# Appending to the tasks.txt file
        # Space placed infront so that the task is added on a new line
        file.write(f"\n{assigned_user}, {task_title}, {task_description}, {current_date}, {due_date}, {completed}")
    print("Task added successfully!")


 # To view all the tasks.
def view_all_tasks():
    with open("tasks.txt", "r") as file:
        tasks = file.readlines()
        if tasks:
            for task in tasks:
                assigned_user, task_title, task_description, assign_date, due_date, completed = task.strip().split(", ")
                print(f"Assigned to: {assigned_user}")
                print(f"Title: {task_title}")
                print(f"Description: {task_description}")
                print(f"Date Assigned: {assign_date}")
                print(f"Due Date: {due_date}")
                print(f"Completed: {completed}")
                print()
        else:
            print("No tasks found.")

# Statistics menu only for the admin 
def display_statistics(username):
    with open("tasks.txt", "r") as file:
        tasks = file.readlines()

        num_tasks = len(tasks)
        
# Reading the user.txt file
    with open("user.txt","r") as file:
            users= file.readlines()
            num_users = len(tasks)

    print(f"Total number of users :{num_users}")
    print(f"Total number of tasks:{num_tasks}")


def view_my_tasks(username):
    with open("tasks.txt", "r") as file:
        tasks = file.readlines()
        user_tasks = []

        for task in tasks:
            assigned_user, task_title, task_description, assign_date, due_date, completed = task.strip().split(", ")
            if assigned_user == username:
                user_tasks.append(task)

        if user_tasks:
            for task in user_tasks:
                assigned_user, task_title, task_description, assign_date, due_date, completed = task.strip().split(", ")
                print(f"Assigned to: {assigned_user}")
                print(f"Title: {task_title}")
                print(f"Description: {task_description}")
                print(f"Date Assigned: {assign_date}")
                print(f"Due Date: {due_date}")
                print(f"Completed: {completed}")
                print()
        else:
            print("No tasks found for this user.")


# Give the user options to proceed.
def main():
    username = login()
    print("Login successful!")
    print()

    while True:
        print("Menu:")
        print("r - Register user")
        print("a - Add task")
        print("va - View all tasks")
        print("vm - View my tasks")
        print("vs-View statistics")
        print("e - Exit")

        option = input("Enter your option: ")

        if option == "r":
           if username == 'admin': # To show that only the admin can register a new user.
                register_user()
           else:
                print("Only admin can register new user.")

        elif option == "a":
            add_task()
        elif option == "va":
            view_all_tasks()

        elif option == "vm":
            view_my_tasks(username)

        elif option == "vs":
            if username == 'admin': # To show that only the admin can view statistics.
                display_statistics(username)
            else:
                print("Only admin can view statistics")

        elif option == "e":
            print("Exiting...")
            break
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()