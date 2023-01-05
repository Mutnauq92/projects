'''
I got clearification and correction from Mr Thabiso Mathebula, HyperionDev Mentor
I was challenge by stripping the "\n" character and thenn splitting the line

Ref: line 181 of "vm" menu option

'''

# =====importing libraries===========
'''This is the section where you will import libraries'''
from datetime import datetime, date

# ====Login Section====
# create a dictionary to confirm login details entered
usernames = {}
with open("user.txt", "r") as open_file:
    for line in open_file:
        clean = line.split(", ")
        usernames[clean[0]] = clean[1].strip("\n")

# print(f"List of user credentials: {usernames}")

# ask the user to enter their username
username = input("Enter your username: ")
# check if username is valid
# if not, close the program
if not username in usernames:
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

# set state for while the user is logged in
logged_in = True
while logged_in:
    # presenting the menu to the user and
    # making sure that the user input is converted to lower case.
    if username == "admin":
        menu = input(
            '''
            Please select one of the following options below:
            r - Registering a user
            ua - user availability
            a - Adding a task
            va - View all tasks
            vm - view my task
            vs - view statistics
            e - Exit : 
            '''
        ).lower()

        if menu == 'r':
            new_user = input("Enter new username: ")
            new_pass = input("Enter new password: ")
            confirm_pass = input("Please confirm password: ")
            # check that username does not already exist
            if not new_user in usernames:
                # check that password is not already in use by one of the users
                # and that the new password is confirmed
                if not new_pass in usernames.values() and confirm_pass == new_pass:
                    # add the new user and password to the user.txt file
                    with open("user.txt", "a") as register_user:
                        register_user.write(f"\n{new_user}, {new_pass}")
                    # update the usernames dictionary
                    usernames[new_user] = new_pass
                    print(f"{new_user} was registered successfully.")
                else:
                    if not confirm_pass == new_pass:
                        print("Passwords do not match.")
                    else:
                        print("Password entered already exists. Please try a different one")
            else:
                print(f"username {new_user} already exists. Please try another username.")

        elif menu == 'ua':

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
                    # if user assigned to a task at line is not in user_names, append user to user_names
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

            # check availability of registered users and print results
            print("List of users and their availability:\n")
            for key, value in user_stats.items():
                # tabs are used for readability when printing results to the user
                if user_stats[key] >= 2:
                    if len(key) >= 6:
                        print(f"{key}:    Unavailable !")
                    else:
                        print(f"{key}:      Unavailable !")
                else:
                    if len(key) >= 6:
                        print(f"{key}:    Available")
                    else:
                        print(f"{key}:      Available")

        elif menu == 'a':
            # create a variable called assigning_tasks and set it to boolean True
            assigning_tasks = True
            while assigning_tasks:
                dt = datetime
                da = date
                assignee = input("Enter assignee's name: ")
                if not assignee in usernames:
                    print("The assignee does not exist.")
                    break
                else:
                    pass
                task_title = input("Enter the title of the task: ").capitalize()
                task_description = input("Enter task description: ").capitalize()
                due_date = input("Enter the due date(eg. 10 October 2020): ")
                current_date = dt.today().strftime("%d %B %Y")
                completion_state = input("Is the task complete: ").capitalize()
                with open("tasks.txt", "a") as open_file:
                    open_file.write(
                        f"\n{assignee}, {task_title}, {task_description},"
                        f" {current_date}, {due_date}, {completion_state}"
                    )
                print("Task was assigned successfully.")
                assigning_tasks = False

            '''In this block you will put code that will allow a user to add a new task to task.txt file
            - You can follow these steps:
                - Prompt a user for the following: 
                    - A username of the person whom the task is assigned to,
                    - A title of a task,
                    - A description of the task and 
                    - the due date of the task.
                - Then get the current date.
                - Add the data to the file task.txt and
                - You must remember to include the 'No' to indicate if the task is complete.'''

        elif menu == 'va':
            with open("tasks.txt") as view_tasks:
                print("Below is a list of all tasks:\n")
                for line in view_tasks:
                    line_list = (line.strip("\n").split(", "))
                    print("Task:                " + line_list[1].capitalize())
                    print("Assigned to:         " + line_list[0])
                    print("Date Assigned:       " + line_list[3])
                    print("Due date:            " + line_list[4])
                    print("Task Complete?       " + line_list[5])
                    print("Task Description:\n  " + line_list[2].capitalize() + "\n")

            '''In this block you will put code so that the program will read the task from task.txt file and
             print to the console in the format of Output 2 presented in the L1T19 pdf file page 6
             You can do it in this way:
                - Read a line from the file.
                - Split that line where there is comma and space.
                - Then print the results in the format shown in the Output 2 in L1T19 pdf
                - It is much easier to read a file using a for loop.'''

        elif menu == 'vm':
            my_tasks = 0
            # check if there are any tasks assigned to user who is logged in
            with open("tasks.txt", "r") as admin_tasks:
                for line in admin_tasks:
                    line_strip = (line.strip("\n").split(", "))
                    if line_strip[0] == username:
                        my_tasks += 1
                    else:
                        pass

            with open("tasks.txt", "r") as admin_tasks:
                if my_tasks > 0:
                    print(f"List of tasks assigned to {username}:\n")
                    for line in admin_tasks:
                        line_list = (line.strip("\n").split(", "))
                        # check if the user is assigned the task at line
                        if not line_list[0] == username:
                            pass
                        else:
                            # print the tasks assigned to user
                            print("Task:                " + line_list[1])
                            print("Assigned to:         " + line_list[0])
                            print("Date Assigned:       " + line_list[3])
                            print("Due date:            " + line_list[4])
                            print("Task Complete?       " + line_list[5])
                            print("Task Description     " + line_list[2] + "\n")
                else:
                    print(f"There are no tasks assigned to {username}")

            '''In this block you will put the code that will read the task from task.txt file and
             print to the console in the format of Output 2 presented in the L1T19 pdf
             You can do it in this way:
                - Read a line from the file
                - Split the line where there is comma and space.
                - Check if the username of the person logged in is the same as the username you have
                read from the file.
                - If they are the same you print the task in the format of output 2 shown in L1T19 pdf '''

        elif menu == 'vs':
            user_names = []
            user_tasks = []
            user_stats = {}
            busy_users = 0
            free_users = 0

            with open("user.txt", "r") as users_file:
                for line in users_file:
                    line_list = line.strip("\n").split(", ")
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

            print("TASK MANAGER STATS ARE DISPLAYED BELOW\n")
            print(f"Total number of tasks:  {sum(user_tasks)}")
            print(f"Total number of users:  {len(user_names)}")
            print(f"Users with tasks:       {busy_users}")
            print(f"Users without tasks:    {free_users}\n")
            print("USER:    NUMBER OF TASKS\n")

            for user, tasks in user_stats.items():
                print(f"{user}:         {tasks}")

        elif menu == 'e':
            print('Goodbye!!!')
            exit()
        else:
            print("You have made a wrong choice, Please Try again")
    elif not username == "admin":
        menu = input(
            '''
            Please select one of the following options below:
            a - Adding a task
            ua - user availability
            va - View all tasks
            vm - view my task
            e - Exit : 
            '''
        ).lower()

        if menu == 'ua':
            user_names = []
            user_tasks = []
            user_stats = {}
            busy_users = 0
            free_users = 0

            with open("user.txt", "r") as users_file:
                for line in users_file:
                    line_list = line.strip("\n").split(", ")
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

            # check availability of registered users
            print("List of users and their availability:\n")
            for key, value in user_stats.items():
                # tabs are used for readability when printing results to the user
                if user_stats[key] >= 2:
                    if len(key) >= 6:
                        print(f"{key}:    Unavailable !")
                    else:
                        print(f"{key}:      Unavailable !")
                else:
                    if len(key) >= 6:
                        print(f"{key}:    Available")
                    else:
                        print(f"{key}:      Available")

        elif menu == 'a':
            assigning_tasks = True
            while assigning_tasks:
                dt = datetime
                da = date
                assignee = input("Enter assignee's name: ")
                if not assignee in usernames:
                    print("The assignee does not exist.")
                    break
                else:
                    pass
                task_title = input("Enter the title of the task: ").capitalize()
                task_description = input("Enter task description: ").capitalize()
                due_date = input("Enter the due date(eg. 10 October 2020): ")
                current_date = dt.today().strftime("%d %B %Y")
                completion_state = input("Is the task complete: ").capitalize()
                with open("tasks.txt", "a") as open_file:
                    open_file.write(
                        f"\n{assignee}, {task_title}, {task_description},"
                        f" {current_date}, {due_date}, {completion_state}"
                    )
                print("Task was assigned successfully.")
                assigning_tasks = False

            '''In this block you will put code that will allow a user to add a new task to task.txt file
            - You can follow these steps:
                - Prompt a user for the following: 
                    - A username of the person whom the task is assigned to,
                    - A title of a task,
                    - A description of the task and 
                    - the due date of the task.
                - Then get the current date.
                - Add the data to the file task.txt and
                - You must remember to include the 'No' to indicate if the task is complete.'''

        elif menu == 'va':
            with open("tasks.txt") as f:
                print("Below is a list of all tasks:\n")
                for line in f:
                    line_list = (line.strip("\n").split(", "))
                    print("Task:                " + line_list[1].capitalize())
                    print("Assigned to:         " + line_list[0])
                    print("Date Assigned:       " + line_list[3])
                    print("Due date:            " + line_list[4])
                    print("Task Complete?       " + line_list[5])
                    print("Task Description:\n  " + line_list[2].capitalize() + "\n")

            '''In this block you will put code so that the program will read the task from task.txt file and
             print to the console in the format of Output 2 presented in the L1T19 pdf file page 6
             You can do it in this way:
                - Read a line from the file.
                - Split that line where there is comma and space.
                - Then print the results in the format shown in the Output 2 in L1T19 pdf
                - It is much easier to read a file using a for loop.'''

        elif menu == 'vm':
            my_tasks = 0
            # check if there are any tasks assigned to user who is logged in
            with open("tasks.txt", "r") as user_task:
                for line in user_task:
                    line_strip = (line.strip("\n").split(", "))
                    if line_strip[0] == username:
                        my_tasks += 1
                    else:
                        pass

            with open("tasks.txt", "r") as user_task:
                if my_tasks > 0:
                    print(f"List of tasks assigned to {username}:\n")
                    for line in user_task:
                        line_list = (line.strip("\n").split(", "))
                        if not line_list[0] == username:
                            pass
                        else:
                            # print the tasks assigned to user
                            print("Task:                " + line_list[1])
                            print("Assigned to:         " + line_list[0])
                            print("Date Assigned:       " + line_list[3])
                            print("Due date:            " + line_list[4])
                            print("Task Complete?       " + line_list[5])
                            print("Task Description     " + line_list[2] + "\n")
                else:
                    print(f"No tasks assigned to {username}.")

            '''In this block you will put the code that will read the task from task.txt file and
             print to the console in the format of Output 2 presented in the L1T19 pdf
             You can do it in this way:
                - Read a line from the file
                - Split the line where there is comma and space.
                - Check if the username of the person logged in is the same as the username you have
                read from the file.
                - If they are the same you print the task in the format of output 2 shown in L1T19 pdf '''

        elif menu == 'e':
            print('Goodbye!!!')
            exit()
        else:
            print("You have made a wrong choice, Please Try again")
