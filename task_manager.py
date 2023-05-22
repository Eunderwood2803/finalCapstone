# Notes:
# 1. Use the following username and password to access the admin rights
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the
# program will look in your root directory for the text files.

# =====importing libraries===========
import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"

# - Store the users in memory
username_password = {}

# - Store the tasks in memory
task_list = []

# - Track if user is logged in
logged_in = False


def username_exists(file_name, new_username):
    with open(file_name, 'r') as read_obj:
        for line in read_obj:
            if new_username in line:
                return True

    return False


def reg_user():
    # - Request input of a new username
    new_username = input("New Username: ")

    # - Request input of a new password
    new_password = input("New Password: ")

    # - Request input of password confirmation.
    confirm_password = input("Confirm Password: ")

    try:
        # - Check if the username already exists
        if username_exists('user.txt', new_username):
            raise Exception(
                'The username already exists. Please add another one: ')

        # - Check ifadmin the new password and confirmed password are the same.
        if new_password == confirm_password:
            # - Add username and password to current username_password dictionary
            username_password[new_username] = new_password

            # - Write the username and password to user.txt
            with open("user.txt", "w") as out_file:
                user_data = []

                for k in username_password:
                    user_data.append(f"{k};{username_password[k]}")

                out_file.write("\n".join(user_data))

            # - If they are the same, add them to the user.txt file,
            print("New user added")

        # - Otherwise you present a relevant message.
        else:
            print("Passwords do no match")

    except Exception as e:
        print(e)


def add_task():
    '''Allow a user to add a new task to task.txt file
        Prompt a user for the following:
            - A username of the person whom the task is assigned to,
            - A title of a task,
            - A description of the task and
            - the due date of the task.'''
    try:
        task_username = ""

        while True:
            task_username = input("Name of person assigned to task: ")

            if task_username not in username_password.keys():
                print("User does not exist. Please enter a valid username")
                continue

            # - Exit the loop if the username exists
            break

        task_title = input("Title of Task: ")
        task_description = input("Description of Task: ")
        task_due_date = input("Due date of task (YYYY-MM-DD): ")
        due_date_time = datetime.strptime(
            task_due_date, DATETIME_STRING_FORMAT)

        # Then get the current date.
        curr_date = date.today()

        ''' Add the data to the file task.txt and
        Include 'No' to indicate if the task is complete.'''
        new_task = {
            "username": task_username,
            "title": task_title,
            "description": task_description,
            "due_date": due_date_time,
            "assigned_date": curr_date,
            "completed": False
        }

        task_list.append(new_task)

        with open("tasks.txt", "w") as task_file:
            task_list_to_write = []

            for t in task_list:
                str_attrs = [
                    t['username'],
                    t['title'],
                    t['description'],
                    t['due_date'].strftime(DATETIME_STRING_FORMAT),
                    t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                    "Yes" if t['completed'] else "No"
                ]
                task_list_to_write.append(";".join(str_attrs))

            task_file.write("\n".join(task_list_to_write))

            print("Task successfully added.")

    except ValueError:
        print("Invalid datetime format. Please use the format specified")


def view_all():
    '''Reads the task from task.txt file and prints to the console in the
    format of Output 2 presented in the task pdf (i.e. includes spacing
    and labelling)
    '''
    for id, task in enumerate(task_list):
        disp_str = f"Task No:\t\t{id}\n"
        disp_str += f"Task:\t\t\t{task['title']}\n"
        disp_str += f"Assigned to:\t\t{task['username']}\n"
        disp_str += f"Date Assigned:\t\t{task['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date:\t\t{task['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Description:\t{task['description']}\n"
        print(disp_str)


def view_mine():
    '''Reads the task from task.txt file and prints to the console in the
    format of Output 2 presented in the task pdf (i.e. includes spacing
    and labelling)
    '''
    # - To be used to validate if a given task belongs to this user
    task_ids = []

    # - Display the list of tasks assigned
    for id, task in enumerate(task_list):
        if task['username'] == curr_user:
            task_ids.append(id)
            disp_str = f"Task No:\t{id}\n"
            disp_str += f"Task:\t\t{task['title']}\n"
            disp_str += f"Assigned to:\t{task['username']}\n"
            disp_str += f"Date Assigned:\t{task['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Due Date:\t{task['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Task Description:\n{task['description']}\n"

            print(disp_str)

    # - Check if any tasks assigned
    if len(task_ids) == 0:
        print("There are no tasks assign to you")
        return

    # - Request the chosen task number
    task_chosen = int(input("Please enter task number: "))

    if task_chosen not in task_ids:
        print("This task is not assigned to you")
        return

    task_item = task_list[task_chosen]

    if task_item['completed'] == False:
        mark_complete = input("Mark the task as complete: Yes/No ").lower()

        if mark_complete == 'yes':
            task_item['completed'] = True
        else:
            edit_the_task = input(
                "Would you like to edit task: Yes/No ").lower()

            if edit_the_task == 'yes':
                task_item['username'] = input("New username: ")
                task_item['due_date'] = datetime.strptime(
                    input("New due date: "), DATETIME_STRING_FORMAT)

        task_list[task_chosen] = task_item

        with open("tasks.txt", "w") as task_file:
            task_list_to_write = []
            for t in task_list:
                str_attrs = [
                    t['username'],
                    t['title'],
                    t['description'],
                    t['due_date'].strftime(DATETIME_STRING_FORMAT),
                    t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                    "Yes" if t['completed'] else "No"
                ]
                task_list_to_write.append(";".join(str_attrs))
            task_file.write("\n".join(task_list_to_write))


def calculate_percentage(dividend, divisor):
    if divisor == 0:
        return 0

    return round(100 * (dividend / divisor))


def generate_reports():
    total_overdue_tasks = 0
    total_completed_tasks = 0
    total_task_uncompleted = 0
    total_tasks = len(task_list)
    current_date = datetime.now()
    incomplete_percentage = 0

    user_tasks_stats = {}

    for task in task_list:
        tasks_stats = user_tasks_stats.get(
            task["username"], {"assigned_tasks": 0, "completed_tasks": 0, "uncompleted_tasks": 0, "overdue_tasks": 0})

        assigned_tasks = tasks_stats.get("assigned_tasks") + 1

        if task['completed']:
            total_completed_tasks += 1
            completed_tasks = tasks_stats.get("completed_tasks") + 1
            tasks_stats.update({"completed_tasks": completed_tasks})
        else:
            total_task_uncompleted += 1
            uncompleted_tasks = tasks_stats.get("uncompleted_tasks") + 1
            tasks_stats.update({"uncompleted_tasks": uncompleted_tasks})

        if (task['completed'] == False and task['due_date'] < current_date):
            total_overdue_tasks += 1
            overdue_tasks = tasks_stats.get("overdue_tasks") + 1
            tasks_stats.update({"overdue_tasks": overdue_tasks})

        tasks_stats.update({"assigned_tasks": assigned_tasks})
        user_tasks_stats.update({task["username"]: tasks_stats})

    incomplete_percentage = (total_task_uncompleted / total_tasks) * 100
    overdue_percentage = (total_overdue_tasks / total_tasks) * 100

    # Print report to file task_overview.txt
    with open("task_overview.txt", "w+") as task_overview:
        task_overview.write("Task Overview\n")
        task_overview.write(
            "-------------------------------------------------------\n")
        task_overview.write(
            f"Total number of tasks: {total_tasks} \n")
        task_overview.write(
            f"Total number of completed tasks: {total_completed_tasks}\n")
        task_overview.write(
            f"Total number of uncompleted tasks: {total_task_uncompleted}\n")
        task_overview.write(
            f"Total number of overdue tasks: {total_overdue_tasks}\n")
        task_overview.write("Overall Summary\n")
        task_overview.write(
            "-------------------------------------------------------\n")
        task_overview.write(
            f"Percentage incomplete: {incomplete_percentage}\n")
        task_overview.write(
            f"Over due percentage: {overdue_percentage}\n")

    user_data = username_password.keys()

    # Print to user_overview.txt
    total_users = len(user_data)

    with open("user_overview.txt", "w+") as user_overview:
        user_overview.write(f"Total number of users: {total_users}\n")
        user_overview.write(
            f"Total number of tracked tasks: {total_tasks}\n\n")

        # iterate over users
        for user in user_data:
            username = user.split(';')[0]
            task = user_tasks_stats.get(username)

            if (task != None):
                user_overview.write(f"User: {username}\n")
                user_overview.write(
                    "-------------------------------------------------------\n")
                user_overview.write(
                    f"Total Tasks: {task.get('assigned_tasks')}\n")
                user_overview.write(
                    f"Total Assigned Tasks: {calculate_percentage(task.get('assigned_tasks'), total_tasks)}\n")
                user_overview.write(
                    f"Percentage Completed Tasks: {calculate_percentage(task.get('completed_tasks'), task.get('assigned_tasks'))}\n")
                user_overview.write(
                    f"Percentage Uncompleted Tasks: {calculate_percentage(task.get('uncompleted_tasks'), task.get('assigned_tasks'))}\n")
                user_overview.write(
                    f"Percentage Overdue Tasks: {calculate_percentage(task.get('overdue_tasks'), task.get('uncompleted_tasks'))}\n\n")


# Create tasks.txt if it doesn't exist
def read_in_task_list():
    if not os.path.exists("tasks.txt"):
        with open("tasks.txt", "w") as default_file:
            pass

    with open("tasks.txt", 'r') as task_file:
        task_data = task_file.read().split("\n")
        task_data = [t for t in task_data if t != ""]

        # - Empty task list array
        task_list = []

        # - Add all tasks to the empty task list array
        for t_str in task_data:
            curr_t = {}

            # Split by semicolon and manually add each component
            task_components = t_str.split(";")
            curr_t['username'] = task_components[0]
            curr_t['title'] = task_components[1]
            curr_t['description'] = task_components[2]
            curr_t['due_date'] = datetime.strptime(
                task_components[3], DATETIME_STRING_FORMAT)
            curr_t['assigned_date'] = datetime.strptime(
                task_components[4], DATETIME_STRING_FORMAT)
            curr_t['completed'] = True if task_components[5] == "Yes" else False

            task_list.append(curr_t)

        # - Return the task list array
        return task_list


def read_in_user_data():
    # If no user.txt file, write one with a default account
    if not os.path.exists("user.txt"):
        with open("user.txt", "w") as default_file:
            default_file.write("admin;password")

    with open("user.txt", 'r') as user_file:
        user_data = user_file.read().split("\n")

        # - Empty username and password dictionary
        username_password = {}

        # - Add all users to the empty dictionary
        for user in user_data:
            username, password = user.split(';')
            username_password[username] = password

        # - Return dictionary
        return username_password


# - Populate in-memory data structures
username_password = read_in_user_data()
task_list = read_in_task_list()

# ====Login Section====
while not logged_in:
    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")

    if curr_user not in username_password.keys():
        print("User does not exist")
        continue
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
        continue
    else:
        print("Login Successful!")
        logged_in = True


while True:
    # presenting the menu to the user and
    # making sure that the user input is converted to lower case.
    print()
    menu = input('''Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my task
gr - Generate reports
ds - Display statistics
e - Exit
: ''').lower()

    if menu == 'r':
        '''Add a new user to the user.txt file'''
        # - Request input of a new username

        reg_user()

    elif menu == 'a':

        add_task()

    elif menu == 'va':
        view_all()

    elif menu == 'vm':
        view_mine()

    elif menu == 'gr':
        generate_reports()

    elif menu == 'ds' and curr_user == 'admin':
        '''If the user is an admin they can display statistics about number of users
            and tasks.'''
        num_users = len(read_in_user_data().keys())
        num_tasks = len(read_in_task_list())

        print("-----------------------------------")
        print(f"Number of users: \t\t {num_users}")
        print(f"Number of tasks: \t\t {num_tasks}")
        print("-----------------------------------")

    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    else:
        print("You have made a wrong choice, Please Try again")
