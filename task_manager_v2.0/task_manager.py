from datetime import date as da

"""
This program keeps track of users, tasks assignment and completion,
Then write reports with user and task statistics.

"""

user_input_file = "user.txt"
task_input_file = "tasks.txt"
task_overview = "task_overview.txt"
user_overview = "user_overview"

# ====Login Section====
# create a dictionary to confirm login details entered
usernames = {}  # usernames are declared globally
tasks_dict = {}


# define a function called read_user_file
# that will usernames from user.txt file and store in usernames dictionary
def read_input_files(user_file, task_file):
    with open(user_file, "r") as open_file:
        for line in open_file:
            clean = line.split(", ")
            # first items of each line are usernames, and the second is the password
            usernames[clean[0]] = clean[1].strip("\n")

    with open(task_file, "r") as f:
        line_count = 0
        for line in f:
            line_strip = line.strip("\n").split(", ")
            tasks_dict[line_count] = line_strip
            line_count += 1


# ask the user to enter their username
def log_in():
    username = input("Enter your username: ")
    # check if username is valid
    # if not, close the program
    if username not in usernames:
        print("Incorrect username entered. The program will now close")
        exit()
    # if username is valid, ask the user to enter the password
    else:
        user_password = input("Enter password: ")
        # if password is incorrect, close the program
        if not user_password == usernames[username]:
            print("Incorrect password. The program will now close")
            exit()
        else:
            print(f"\nWelcome to Task Manager\nYou are logged in as {username}")
    return username


def task_menu():
    # number of task is used to output to the user the range of tasks to select from
    number_of_tasks = len(tasks_dict)
    tasks_menu = int(input(
        f"""
        Enter a number between 0 and {number_of_tasks - 1} to select a corresponding task
        Or enter -1 to go back to main menu
        """
    ))

    if tasks_menu == (-1):
        print(f"Returning to {user_name} main menu.")
        run_program(user_name)
    else:
        edit_task(tasks_menu)


def reg_user(credential_dictionary):
    new_user = ""
    # check that username does not already exist
    tries_count = 3
    while tries_count > 0:
        new_user = input("Enter a new username: ")
        if new_user not in credential_dictionary:
            tries_count = 0
        else:
            tries_count -= 1
            if tries_count == 0:
                print("No more tries. try running the program again: ")
                exit()
            else:
                print("username already exists. try a different one.")
    else:
        new_pass = input("Enter a new password: ")
        if new_pass not in credential_dictionary:
            confirm_pass = input("Please confirm the password: ")
            if confirm_pass != new_pass:
                print("Passwords don't match. Please try registering again.")
            else:
                usernames[new_user] = new_pass
                with open(user_input_file, "a") as register_user:
                    register_user.write(f"\n{new_user}, {new_pass}")
                print("User registration successful.")

        else:
            print("Password is already in use by another user. Try registering with a different password.")


# define a function that changes the date from string to int
# to enable counting days overdue of the tasks
def convert_date(string_date, new_date_list):
    for item in string_date.split(" "):
        # cast list items to int for later calculation
        new_date_list.append(int(item))


def split_date(use_date):
    temp_list = []

    for item in use_date.split("-"):
        temp_list.append(int(item))

    temp_date = da(temp_list[0], temp_list[1], temp_list[2])

    return temp_date


def add_task():
    # create a variable called assigning_tasks and set it to boolean True
    assigning_tasks = True
    while assigning_tasks:
        assignee = input("Enter assignee's name: ")
        if assignee not in usernames:
            print("The assignee does not exist.")
            break
        else:
            task_title = input("Enter the title of the task: ").capitalize()
            task_description = input("Enter task description: ").capitalize()
            due_date = input("Enter the due date(eg. 2022 12 31): ")
            current_date = da.today()
            due_date_list = []
            convert_date(due_date, due_date_list)
            use_due_date = da(due_date_list[0], due_date_list[1], due_date_list[2])
            completion_state = input("Is the task complete: ").capitalize()

            with open(task_input_file, "a") as open_file:
                open_file.write(
                    f"\n{assignee}, {task_title}, {task_description},"
                    f" {current_date}, {use_due_date}, {completion_state}"
                )

            print("Task was assigned successfully.")

            assigning_tasks = False

        read_input_files(user_input_file, task_input_file)


def edit_task(task):
    if tasks_dict[task][-1] == "No":
        # display the selected task to the user
        print(
            f"\nSelected task:       Task {task}"
            f"\nTask:                {tasks_dict[task][1]}"
            f"\nAssigned to:         {tasks_dict[task][0]}"
            f"\nDate Assigned:       {tasks_dict[task][3]}"
            f"\nDue date:            {tasks_dict[task][4]}"
            f"\nTask Complete?       {tasks_dict[task][-1]}"
            f"\nTask Description     {tasks_dict[task][2]}"
        )
        # let the user choose what edit they want to perform on the selected task
        choose_edit = input(
            """
            Select an option from the menu below:
            un - edit task assignee
            dd - edit task due date
            tc - edit task completion status
            c - cancel task editing
            """
        )
        if choose_edit == "un":
            new_assignee = input("Enter the new assignee: ")

            if new_assignee in usernames.keys():
                with open(task_input_file, "r") as rf:
                    read_lines = rf.readlines()
                    with open(task_input_file, "w") as wf:
                        # update the value at the specified task
                        read_lines[task] = f"{new_assignee}, {', '.join(tasks_dict[task][1::])}\n"
                        wf.writelines(read_lines)

                # read_input_files(user_input_file, task_input_file)
                print("New assignee was edited successfully ✓.")
                task_menu()

            else:
                print(f"\nuser {new_assignee} has not been created yet. Enter another assignee.")
                edit_task(task)

        elif choose_edit == "dd":
            due_date = input("Enter the due date(eg. 2022 12 31): ")
            due_date_list = []
            convert_date(due_date, due_date_list)
            use_due_date = da(due_date_list[0], due_date_list[1], due_date_list[2])

            with open(task_input_file, "r") as rf:
                read_lines = rf.readlines()
                with open(task_input_file, "w") as wf:
                    read_lines[task] = f"{', '.join(tasks_dict[task][:4])}, {use_due_date}, {tasks_dict[task][5]}\n"
                    wf.writelines(read_lines)

            # read_input_files(task_input_file, user_input_file)
            print(f"New due date was edited successfully ✓.")
            task_menu()

        elif choose_edit == "tc":
            complete_task = input("Is the task complete? ").capitalize()
            with open(task_input_file, "r") as rf:
                read_lines = rf.readlines()
                # open tasks file in write mode while open in read mode
                with open(task_input_file, "w") as wf:
                    # change the data on the selected task and write it back to tasks file
                    read_lines[task] = f"{', '.join(tasks_dict[task][:5])}, {complete_task}\n"
                    # write the lines back to tasks text file
                    wf.writelines(read_lines)

            # read_input_files(task_input_file, user_input_file)
            print(f"Task completion status was edited successfully ✓.")
            task_menu()

        elif choose_edit == "c":
            print("Returning to task menu")
            task_menu()

        else:
            print("Invalid operation selected")
    else:
        print(
            f"Task {task} cannot be edited. It has already been completed.\n"
            f"Please select another task."
        )
        task_menu()


def view_all(tasks_dictionary):
    read_input_files(user_input_file, task_input_file)
    # loop through the tasks_dictionary to view all tasks
    print("\nList of all tasks")
    for key, value in tasks_dictionary.items():
        print(
            f"\nTask {key}"
            f"\nTask:                {value[1]}"
            f"\nAssigned to:         {value[0]}"
            f"\nDate Assigned:       {split_date(value[3]).strftime('%d %B %Y')}"
            f"\nDue date:            {split_date(value[4]).strftime('%d %B %Y')}"
            f"\nTask Complete?       {value[-1]}"
            f"\nTask Description     {value[2]}"
        )

    task_menu()


def view_mine(task_dict, logged_in_user):
    read_input_files(user_input_file, task_input_file)
    # create a list to store logged-in user's tasks
    my_tasks = []
    for key, value in task_dict.items():
        if tasks_dict[key][0] == logged_in_user:
            my_tasks.append(key)

    # initialize a counter to keep track of how many tasks the user has
    task_counter = 0

    # loop through temporary list of tasks assigned to the user
    print(f"\nTasks assigned to {logged_in_user}")
    if len(my_tasks) > 0:
        for task in my_tasks:
            print(
                f"\nTask {task_counter}"
                f"\nTask:                {tasks_dict[task][1]}"
                f"\nAssigned to:         {tasks_dict[task][0]}"
                f"\nDate Assigned:       {split_date(tasks_dict[task][3]).strftime('%d %B %Y')}"
                f"\nDue date:            {split_date(tasks_dict[task][4]).strftime('%d %B %Y')}"
                f"\nTask Complete?       {tasks_dict[task][-1]}"
                f"\nTask Description     {tasks_dict[task][2]}"
            )
            task_counter += 1

        return my_tasks

    else:
        print(f"There are no tasks assigned to {logged_in_user}")


def get_stats():
    user_names = []
    user_tasks = []
    complete_tasks = []
    incomplete_tasks = []
    over_due_tasks = 0
    user_stats = {}
    busy_users = 0
    free_users = 0
    current_date = da.today()

    # append 0 to all indexes corresponding to user_names indexes
    # these will be incremented later when user tasks are counted
    for user in usernames:
        user_names.append(user)
        user_tasks.append(0)
    # read through the tasks.txt file and append
    # completed and incomplete tasks to their respective list
    with open(task_input_file, "r") as tasks_file:
        for line in tasks_file:
            line_strip = line.strip("\n").split(", ")
            # if task_completion status is no, then append the task to incomplete tasks list
            if line_strip[-1] == "No":
                incomplete_tasks.append(line_strip)
                # for every incomplete task, if due date has passed, increment incomplete tasks by 1
                if (split_date(line_strip[4]) - current_date).days < 0:
                    over_due_tasks += 1
                else:
                    pass
            elif line_strip[-1] == "Yes":
                complete_tasks.append(line_strip)
            for user_index in range(len(user_names)):
                # count each appearance of username and increment the counter accordingly
                # increment the task count for each user in user_names
                if line_strip[0] == user_names[user_index]:
                    user_tasks[user_index] += 1

    # insert keys and values into the user_stats dictionary
    for user_index in range(len(user_names)):
        user_stats[user_names[user_index]] = user_tasks[user_index]

    # count busy users and free users
    for user in user_names:
        if user_stats[user] > 0:
            busy_users += 1
        else:
            free_users += 1

    return usernames, user_tasks, user_stats, busy_users, free_users, complete_tasks, incomplete_tasks, over_due_tasks


def display_stats():
    # define a function that displays stats
    def show_stats():
        # create tasks_overview and user_overview dictionaries
        # to store data from task_overview.txt and user_overview.txt respectively
        tasks_overview_dict = {}
        user_overview_dict = {}

        # print tasks_overview.txt file to the user
        with open("task_overview.txt", "r", encoding="utf-8-sig") as rf:
            for line in rf:
                line_split = line.strip("\n").split(", ")
                # use the first item on each line as a key to respective dictionary
                tasks_overview_dict[line_split[0]] = line_split[1]

        # print user_overview.txt file to the user
        with open("user_overview.txt", "r", encoding="utf-8-sig") as rf:
            for line in rf:
                line_split = line.strip("\n").split(", ")
                user_overview_dict[line_split[0]] = line_split[1::]


        print(
            f"""
        TASKS OVERVIEW
        Number of tasks:                        {tasks_overview_dict['tasks']}
        Number of completed tasks:              {tasks_overview_dict['completed']}
        Number of incomplete tasks:             {tasks_overview_dict['incomplete']}
        Number of overdue incomplete tasks:     {tasks_overview_dict['overdue tasks']}
        Percentage of incomplete tasks:         {tasks_overview_dict['percentage incomplete']}
        Percentage of completed tasks:          {tasks_overview_dict['percentage completed']}

        
        USERS OVERVIEW
        Total number of user                    {len(usernames)}
        Total number of tasks                   {len(tasks_dict)}
        
        USER      TASKS     TASKS(%)   COMPLETED(%)  INCOMPLETE(%)   OVERDUE(%)
        """
        )
        for user in user_overview_dict:
            this_user = user_overview_dict[user]
            if float(this_user[0]) > 0:
                print(
                    f"      {user}"
                    f"         {user_overview_dict[user][0]}"
                    f"        {user_overview_dict[user][1]}"
                    f"         {user_overview_dict[user][2]}"
                    f"         {user_overview_dict[user][3]}"
                    f"            {user_overview_dict[user][4]}"
                )
            else:
                print(
                    f"      {user}"
                    f"         {user_overview_dict[user][0]}"
                    f"        {user_overview_dict[user][1]}"
                    f"           {0.0}"
                    f"          {0.0}"
                    f"             {0.0}"
                )

    # first generate reports and then call the function to display the stats
    generate_reports()
    show_stats()


def user_availability():
    # create empty lists called, user_names, user_tasks
    # - a dictionary called user_stats
    # - variables called busy_users and free_users to count
    # - users that have been assigned tasks and those who haven't
    user_names = []
    user_tasks = []
    user_stats = {}
    busy_users = 0
    free_users = 0

    with open("user.txt", "r") as users_file:
        for line in users_file:
            line_list = line.strip("\n").split(", ")
            # if user assigned to a task at line is not in user_names list, append user to user_names
            if not line_list[0] in user_names:
                user_names.append(line_list[0])
            else:
                pass

    # append 0 to all indexes corresponding to user_names indexes
    # these will be incremented later when user tasks are counted
    for user in user_names:
        user_tasks.append(0)

    with open("tasks.txt", "r") as tasks_file:
        for line in tasks_file:
            line_strip = line.strip("\n").split(", ")
            for user_index in range(len(user_names)):
                # increment the task count for each user in user_names
                if line_strip[0] == user_names[user_index]:
                    user_tasks[user_index] += 1

    # insert values into the user_stats dictionary
    for user in range(len(user_names)):
        user_stats[f"{user_names[user]}"] = user_tasks[user]

    # count busy users and free users
    for user in user_names:
        if user_stats[user] > 0:
            busy_users += 1
        else:
            free_users += 1
    print(
        f"Busy Users:       {busy_users}\n"
        f"Available Users:  {free_users}\n"
    )
    # check availability of registered users and print results
    print("List of users and their availability:\n")
    for key, value in user_stats.items():
        # tabs are used for readability when printing results to the user
        # if user has more than 2 task assigned to them and are incomplete
        # mark the user as unavailable
        if user_stats[key] >= 2:
            if len(key) >= 6:
                print(f"{key}:      Unavailable !")
            else:
                print(f"{key}:      Unavailable !")
        else:
            if len(key) >= 6:
                print(f"{key}:      Available")
            else:
                print(f"{key}:      Available")


def generate_reports():
    stats_dict = get_stats()[2]
    incomplete_user_tasks = {}
    complete_user_tasks = {}
    overdue_user_tasks = {}

    for user in usernames:
        incomplete_user_tasks[user] = 0
        complete_user_tasks[user] = 0
        overdue_user_tasks[user] = 0

        for task in tasks_dict:
            if tasks_dict[task][0] == user and tasks_dict[task][-1] == "No":
                incomplete_user_tasks[user] += 1
                if (split_date(tasks_dict[task][4]) - da.today()).days <= 0:
                    overdue_user_tasks[user] += 1
                else:
                    pass
            elif tasks_dict[task][0] == user and tasks_dict[task][-1] == "Yes":
                complete_user_tasks[user] += 1

    # create tasks_overview.txt file and write its content
    with open("task_overview.txt", "w", encoding="utf-8-sig") as wf:
        wf.write(
            f"tasks, {len(tasks_dict)}\n"
            f"completed, {len(get_stats()[5])}\n"
            f"incomplete, {len(get_stats()[6])}\n"
            f"overdue tasks, {get_stats()[7]}\n"
            f"percentage incomplete, {round((len(get_stats()[6]) / len(tasks_dict)) * 100, 2)}%\n"
            f"percentage completed, {round((len(get_stats()[5]) / len(tasks_dict)) * 100, 2)}%\n"
        )
    # create user_overview.txt file and write its content

    # loop through each user
    with open("user_overview.txt", "w", encoding="utf-8-sig") as wf:
        for user in usernames:
            if stats_dict[user] > 0:
                wf.write(
                    f"{user}, {stats_dict[user]}, {round((((stats_dict[user]) / len(tasks_dict)) * 100), 2)}, "
                    f"{round(((complete_user_tasks[user] / stats_dict[user]) * 100), 2)}, "
                    f"{round(((incomplete_user_tasks[user] / stats_dict[user]) * 100), 2)}, "
                    f"{round(((overdue_user_tasks[user] / stats_dict[user]) * 100), 2)}\n"
                )
            elif stats_dict[user] == 0:
                wf.write(
                    f"{user}, {stats_dict[user]}, {round((((stats_dict[user]) / len(tasks_dict)) * 100), 2)}, "
                    f"0, "
                    f"0, "
                    f"0\n"
                )

    print("\ntasks_overview and user_overview reports generated successfully ✓")


# define a function called run_program that contains all the functionality of tas_manager.py
def run_program(current_user):
    # define a function that will display menu according to the user that is logged in
    def main_menu(signed_in_user):
        if signed_in_user == "admin":
            menu = input(
                f'''
                {signed_in_user.capitalize()} main menu
                Please select one of the following options:
                r - register user
                vu - view users
                ua - user availability
                a - add task
                va - view all tasks
                vm - view my tasks
                gr - generate reports
                ds - display statistics
                e - exit
                '''
            ).lower()

            return menu
        else:
            menu = input(
                f'''
                {signed_in_user.capitalize()} main menu
                Please select one of the following options:
                vu - view users
                ua - user availability
                a - add task
                va - view all tasks
                vm - view my tasks
                e - exit
                '''
            ).lower()
            return menu

    while current_user:
        # presenting the menu to the user and
        # making sure that the user input is converted to lower case.
        if user_name == "admin":
            main_user_menu = main_menu(user_name)

            if main_user_menu == 'r':
                reg_user(usernames)  # parse in the usernames dictionary

            elif main_user_menu == 'ua':
                user_availability()

            elif main_user_menu == "vu":
                print("List of users:")
                for user in usernames:
                    print(f"{user}")

            elif main_user_menu == 'a':
                add_task()

            elif main_user_menu == 'va':
                if not len(tasks_dict) > 0:
                    print(f"Please check that the the {task_input_file} is not empty.")
                else:
                    view_all(tasks_dict)

            elif main_user_menu == 'vm':
                view_mine(tasks_dict, user_name)

            elif main_user_menu == 'ds':
                display_stats()

            elif main_user_menu == "gr":
                generate_reports()

            elif main_user_menu == 'e':
                print('Goodbye!!!')
                exit()
            else:
                print("\nYou have made a wrong choice, Please Try again")

        elif not user_name == "admin":
            main_user_menu = main_menu(user_name)

            if main_user_menu == 'r':
                reg_user(usernames)  # parse in the usernames dictionary

            elif main_user_menu == 'ua':
                user_availability()

            elif main_user_menu == "vu":
                print("List of users:")
                for user in usernames:
                    print(f"{user}")

            elif main_user_menu == 'a':
                add_task()

            elif main_user_menu == 'va':
                if not len(tasks_dict) > 0:
                    print(f"Please check that the the {task_input_file} is not empty.")
                else:
                    view_all(tasks_dict)

            elif main_user_menu == 'vm':
                view_mine(tasks_dict, user_name)

            elif main_user_menu == 'e':
                print('Goodbye!!!')
                exit()
            else:
                print("\nYou have made a wrong choice, Please Try again")


# read input files and store values in dedicated dictionaries
read_input_files(user_input_file, task_input_file)

stats_dict = get_stats()
# set state for while the user is logged in
user_name = log_in()

logged_in = True

run_program(logged_in)
