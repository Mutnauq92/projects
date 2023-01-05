from tabulate import tabulate


# ========The beginning of the class==========
class Shoe:

    def __init__(self, country, code, product, cost, quantity):
        self.country = country
        self.code = code
        self.product = product
        self.cost = cost
        self.quantity = quantity

    def get_cost(self):
        return self.cost

    def get_quantity(self):
        return self.quantity

    def __str__(self):
        return f"{self.country}, {self.code}, {self.product}, {self.cost}, {self.quantity}"


shoe_list = []
inventory_file = "inventory.txt"
shoe_codes_dict = {}


def read_shoes_data(input_file):
    with open(input_file, "r") as f:
        for index, line in enumerate(f):
            # use if statement to skip the first file of the input file
            if index == 0:
                pass
            else:
                try:
                    line_split = line.strip("\n").split(",")
                    # create an alias variable for line_split for code readability
                    ls = line_split
                    # check that the line has all required arguments
                    # if not, then let the user know that the line is missing argument(s)
                    if len(line_split) < 5:
                        print(f"Line {index} Logical error: Missing one or more of required arguments.")
                    else:
                        # create a Shoe object for each of the lines
                        shoe_object = Shoe(ls[0], ls[1], ls[2], ls[3], ls[4])
                        shoe_list.append(f"{shoe_object}")
                        shoe_codes_dict[f"{ls[1]}"] = f"{ls[2]}"
                except ValueError as ve:
                    print(ve)


def capture_shoes():
    shoe_capture = True
    while shoe_capture:
        try:
            shoe_country = input("Enter name of the country: ")
            shoe_code = input("Enter shoe code: ").upper()

            while True:
                if shoe_code in shoe_codes_dict:
                    shoe_code = input("The shoe code is already in use. Try again: ").upper()
                else:
                    break

            shoe_name = input("Enter name of the product: ")
            shoe_cost = float(input("Enter shoe cost: "))
            shoe_quantity = int(input("Enter shoe quantity: "))
            temp_list = [shoe_country, shoe_code, shoe_name, shoe_cost, shoe_quantity]
            tl = temp_list

            new_shoe = f"{Shoe(tl[0],tl[1],tl[2],tl[3],tl[4])}"
            country, code, name, cost, qty = new_shoe.split(", ")

            with open(inventory_file, "a") as f:
                f.write(f"\n{country},{code},{name},{cost},{qty}")

            print("Shoe captured successfully ✔")
            shoe_list.clear()
            read_shoes_data(inventory_file)

            another_shoe = input("Do you want to add another shoe (y / n )? ").lower()

            if another_shoe == "y":
                capture_shoes()
            elif another_shoe == "n":
                print("Returning to main menu !")
                shoe_capture = False
            else:
                print("Invalid input. Returning to main menu...")
                shoe_capture = False
            break

        except ValueError as ve:
            print("Invalid input on cost and quantity values.")


def view_all():
    shoe_grid = []
    headers = ["COUNTRY", "CODE", "PRODUCT", "COST", "QUANTITY"]
    for item in shoe_list:
        shoe_grid.append(item.split(", "))

    print(tabulate(shoe_grid, headers=headers, tablefmt="fancy_grid"))
    # print(len(shoe_list))


def re_stock(parsed_list):
    # clear the old shoe_list
    shoe_list.clear()
    # call read_shoe_data to append updated shoe data to shoe_list
    read_shoes_data(inventory_file)
    # create a temporary list to store shoe quantities only
    quantities = []
    shoe_grid = []

    # append shoe quantities to the temporary quantities list
    for index, shoe in enumerate(parsed_list):
        quantities.append(int(parsed_list[index].split(", ")[4]))

    # define a function called "smallest" to find the smallest shoe quantity
    def smallest(in_list):
        # create a temporary variable to store the smallest value
        temp_min = 0
        # enumerate through the shoe list and assign the smallest value to temp_min
        for num_index, num in enumerate(in_list):
            if num_index == 0:
                if num < in_list[num_index + 1]:
                    temp_min = num
                else:
                    temp_min = in_list[num_index + 1]
            elif 0 < num_index < len(in_list) - 2:
                if temp_min < num:
                    temp_min = temp_min
                else:
                    temp_min = num
            elif num_index == len(in_list) - 1:
                if temp_min < num:
                    temp_min = temp_min
                else:
                    temp_min = num

        return temp_min, in_list.index(temp_min)

    # create a variable to store the data of the shoe with smallest quantity
    lowest_qty_shoe = shoe_list[smallest(quantities)[1]]
    shoe_name = lowest_qty_shoe.split(', ')[2]
    shoe_qty = lowest_qty_shoe.split(', ')[-1]
    shoe_code_low = lowest_qty_shoe.split(', ')[1]
    headers = ["SHOE_NAME", "SHOE_CODE", "QTY"]
    shoe_grid.append([shoe_name, shoe_code_low, shoe_qty])
    print("MOST BOUGHT SHOE")
    print(tabulate(shoe_grid, headers=headers, tablefmt="fancy_grid"))

    return smallest(quantities)


def update_qty(input_file, index, add_qty):
    with open(input_file, "r") as rf:
        read_lines = rf.readlines()

        with open(input_file, "w") as wf:
            # update the desired line in the text file
            # original_shoe = read_lines[index + 1]
            current_qty = read_lines[index + 1].split(',')[-1]
            updated_qty = f"{int(current_qty) + add_qty}"
            read_lines[index + 1] = f"{read_lines[index + 1].replace(current_qty, updated_qty)}\n"
            wf.writelines(read_lines)

    read_shoes_data(inventory_file)


def search_shoe():
    # then create a temporary shoe_shelf list to store the values to be printed.
    # create a temporary shoe_details dictionary to store shoe code and shoe name
    shoe_shelf = []
    shoe_details = []
    shoe_codes = []
    shoes_dict = {}
    for index, num in enumerate(shoe_list):
        # append the shoe codes and their names to shoe_details list
        # then append the codes only to shoe_codes list
        shoe_details.append([f"{num.split(', ')[1]}, {num.split(', ')[2]}"])
        shoe_codes.append(num.split(", ")[1])
        shoes_dict[f"{num.split(', ')[1]}"] = num.split(', ')[2]

    shoe_code = input("Please enter the shoe code: ").upper()

    try:
        shoe_name = shoes_dict[shoe_code]
        shelf_number = shoe_codes.index(shoe_code)
        stock_qty = shoe_list[shelf_number].split(', ')[-1]
        shoe_shelf.append([shoe_code, shoe_name, shelf_number, stock_qty])
        print(tabulate(shoe_shelf, headers=["SHOE_CODE", "SHOE_NAME", "SHELF #", "QTY"], tablefmt="fancy_grid"))

    except KeyError:
        print("Shoe code not found !")

    finally:
        pass


def value_per_item():
    # create header values to print with tabulate module
    headers = ["SHOE_NAME", "STOCK_VALUE"]
    values = []
    # value_grid = []
    for each_shoe in shoe_list:
        # cast the current string shoe cost values to float
        value = float(each_shoe.split(", ")[3]) * float(each_shoe.split(", ")[4])
        values.append([each_shoe.split(', ')[2], f"R{round(value, 2)}"])

    print(tabulate(values, headers=headers, tablefmt="fancy_grid"))


def highest_qty(in_list):
    # base case: check if there is only 1 number left from the list
    if len(in_list) == 1:
        # if only 1 number is left, return that number
        return in_list[0]
    else:
        # compare item at index 0 and index 1, and pop the smallest between the two
        # and then call the function again, with new list
        if int(in_list[0].split(", ")[4]) > int(in_list[1].split(", ")[4]):
            in_list.pop(1)
            return highest_qty(in_list)
        elif int(in_list[0].split(", ")[4]) == int(in_list[1].split(", ")[4]):
            in_list.pop(1)
            return highest_qty(in_list)
        else:
            in_list.pop(0)
            return highest_qty(in_list)


def start_program(menu):
    shoe_list.clear()
    read_shoes_data(inventory_file)

    if menu == "cap":
        capture_shoes()

    elif menu == "va":
        view_all()

    elif menu == "vals":
        value_per_item()

    elif menu == "re":
        qty, index = re_stock(shoe_list)

        update_shoe_qty = input("Do you want to add more stock(y / n)? ").lower()
        if update_shoe_qty == "y":
            new_qty = int(input("Enter the additional: "))
            update_qty(inventory_file, index, new_qty)
            print("Shoe quantity updated successfully ✔")
        elif update_shoe_qty == "n":
            print(f"Quantity of {shoe_list[index].split(',')[2]} remains unchanged.")
        else:
            print("Invalid input. Returning to main menu...")

    elif menu == "ss":
        search_shoe()

    elif menu == "fs":
        # create a variable for the shoe object with the highest quantity
        shoe = highest_qty(shoe_list).split(", ")[2]
        shoe_qty = highest_qty(shoe_list).split(", ")[-1]
        print(f"{shoe} is up for sale !!! There are {shoe_qty} available nationwide !!!")

    elif menu == "e":
        print("Goodbye !!!")
        exit()

    else:
        print("Invalid input")


def main_menu():
    user_choice = input(
        f"""
            Choose an operation from the menu below:
            cap - capture a new product
            va  - view all products
            re  - re-stock product
            ss  - search for a product
            vals - value per item
            fs - for sale
            e - exit the program

        """).lower()

    return user_choice


while True:

    start_program(main_menu())
