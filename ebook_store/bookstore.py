import sqlite3
from sqlite3 import Error
from tabulate import tabulate


class DBMS:
    """
    This is a Database Management System
    Actions that can be performed with books:
        1. Add
        2. Update
        3. Delete
        4. Search
        5. Display all books
    """

    def __init__(self, db_file, book_id=None, title=None, author=None, qty=None):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.qty = qty

        try:
            self.db = sqlite3.connect(db_file)
            self.cursor = self.db.cursor()
            books = """
                create table if not exists books(
                    'book_id' varchar(20) not null primary key,
                    'title' varchar(20) not null,
                    'author' varchar(20) not null,
                    'qty' integer not null
                )
            """
            self.cursor.execute(books)
            self.db.commit()
        except Error as e:
            print(e)

    def insert_book(self, book_id, title, author, qty):
        """
        This function inserts a book into 'ebookstore' database
        :param book_id: Inserts a book_id value
        :param title:   Inserts a book title
        :param author:  Inserts the name of the author
        :param qty:     Inserts the quantity of books

        """
        try:
            with self.db:
                new_book = """
                    insert into books
                    values(?, ?, ?, ?)
                """
                self.cursor.execute(new_book, (book_id, title, author, qty))
        except sqlite3.IntegrityError as ie:
            print(f"Book_ID already exists. Please choose update, or enter a different book_id !!!")

    def id_update(self):
        """
        This function updates the book_id.
        :return: Does not return anything
        """
        title = input("Enter the book title: ")
        try:
            book_id = input("Enter a new book_id: ")
            update_book = """
                update books
                set book_id = ? where title = ?
            """
            self.cursor.execute(update_book, (book_id, title))
            print("Book updated.")
        except Error as e:
            print(e)

    def title_update(self):
        """
        This function updates the title of a book.
        :return: Nothing returned
        """

        book_id = input("Enter the book_ID: ")
        try:
            title = input("Enter a new title: ")
            # check if the book with entered title exists and execute the required query
            update_book = """
                            update books
                            set title = ? where book_id = ?
                        """
            self.cursor.execute(update_book, (title, book_id))
            print("Book updated.")
        except Error as e:
            print(e)

    def author_update(self):
        """
        This function updates book author
        :return: Nothing returned
        """
        book_id = input("Enter the book_ID: ")
        try:
            author = input("Enter new author: ")
            update_book = """
                update books
                set author = ? where book_id = ?
            """
            self.cursor.execute(update_book, (author, book_id))
            print("Book updated.")
        except Error as e:
            print(e)

    def qty_update(self):
        """
        This function updates book quantity
        :return: Does not return anything
        """
        book_id = input("Enter the book_ID: ")
        try:
            self.cursor.execute("""select title, qty from books where book_id = ?""", (book_id,))
            result = self.cursor.fetchall()
            title, qty = result[0]
            headers = ["TITLE", "QUANTITY"]
            print(tabulate(result, headers=headers, tablefmt="simple_grid", numalign="center", stralign="center"))
            qty = int(input("Enter number of books to add"))
            update_book = """
                update books
                set qty = (qty + ?) where book_id = ?
            """
            self.cursor.execute(update_book, (qty, book_id))
            print("Book updated.")
        except Error as e:
            print(e)

    def update_book(self):
        """
        This function updates book_ID, title, author and qty (Quantity):
        """
        detail_update = input("""
        What would you like to update:
        1. book_id
        2. title
        3. author
        4. qty
        """)
        if detail_update == "1":
            self.id_update()
        elif detail_update == "2":
            self.title_update()
        elif detail_update == "3":
            self.author_update()
        elif detail_update == "4":
            self.qty_update()

    def delete_book(self, del_id):
        book_shelf = []
        book = """
                select title, qty from books where book_id = ?
                """
        self.cursor.execute(book, (del_id,))
        result = self.cursor.fetchall()
        book_shelf.append(result)
        title, qty = book_shelf[0][0]

        confirm_deletion = input(f"""
            Title: {title}
            Copies: {qty}
            Continue delete? y/n? 
        """)
        if confirm_deletion == "y":
            del_book = """delete from books where book_id = ?"""
            self.cursor.execute(del_book, (del_id,))
            print("Book deleted !")
        else:
            print("No change made to the database. Goodbye !")

    def search_book(self, book_id, title):
        """
        Book_ID and Title will both be used to look for either:
        Exact title and exact book_id will be search.
        :param book_id: Used to search a book with this book_ID
        :param title: Used to search a book with this title
        :return: Does not return anything
        """
        book_list = """
            select * from books where book_id = ? or title = ?
        """
        with self.db:
            try:
                self.cursor.execute(book_list, (book_id, title))
                result = conn.cursor.fetchall()
                headers = ["BOOK_ID", "TITLE", "AUTHOR", "QTY"]
                print(
                    tabulate(
                        result, headers=headers,
                        tablefmt="simple_grid",
                        stralign="center", numalign="center")
                )
            except Error as e:
                print(e)

    @property
    def get_books(self):
        book_list = """
            select * from books order by book_id;
        """
        with self.db:
            self.cursor.execute(book_list)
            result = conn.cursor.fetchall()
            headers = ["BOOK_ID", "TITLE", "AUTHOR", "QTY"]
            print(
                tabulate(
                    result, headers=headers,
                    tablefmt="simple_grid",
                    stralign="center", numalign="center")
            )


conn = DBMS("ebookstore")


def main_menu():
    choice = input("""
    Choose operation below:
    1. Enter book
    2. Update book
    3. Delete book
    4. Search book
    5. Show books
    0. exit the program
    """)

    return choice


def run():
    """
    This is the main program
    :return:
    """
    while True:
        user_choice = main_menu()

        if user_choice == "":
            print("You did not make a choice.")

        elif user_choice == "1":
            print("Enter new book details:")
            book_id = input("Enter book_id: ")
            title = input("Enter title: ")
            author = input("Enter author name: ")
            qty = int(input("Enter # of copies: "))
            try:
                conn.insert_book(book_id, title, author, qty)
            except Error as e:
                print(e)

        elif user_choice == "2":
            conn.update_book()

        elif user_choice == "3":
            book_id = int(input("Enter book_id to delete: "))
            conn.delete_book(book_id)

        elif user_choice == "4":
            book_id = input("Enter book_id: ")
            title = input("Enter the title: ")
            conn.search_book(book_id, title)

        elif user_choice == "5":
            conn.get_books

        elif user_choice == "0":
            conn.db.close()
            print("Closing database... Goodbye !")
            exit()


run()
