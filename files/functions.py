# File contains all functions that are called from main.py

import sqlite3
from files import plu_produce


# MENUS

def menu():
    """Displays the main menu for the program."""
    welcome = "Welcome to your Produce Inventory Assistant, PIA!"
    more_info = "Type 'help' for more info."
    line = "-" * len(welcome)
    spacer = "\n"
    print(spacer)
    print(line)
    print(welcome)
    print(more_info)


def help_menu():
    """Displays the contents in the help.txt file."""
    f = open("./files/help.txt")
    lines = f.readlines()

    for line in lines:
        print(line.strip())


def pia():
    """Displays the contents in the README.md file."""
    f = open('README.md')
    lines = f.readlines()

    for line in lines:
        print(line.strip())


# INITIALIZING FUNCTIONS

def connect_db():
    """Connects to the produce.db file and returns the connection."""
    conn = sqlite3.connect("./files/produce.db")
    return conn


def create_table_produce(conn):
    """Attempts to create table 'produce' in produce.db file.

    Raises:
        sqlite3.OperationalError: If table 'produce' already created; pass.

    """
    try:
        sql = 'CREATE table produce (name, code, stock, price)'
        conn.execute(sql)
    except sqlite3.OperationalError:
        pass


def create_table_orders(conn):
    """Attempts to create table 'orders' in produce.db file.

    Raises:
        sqlite3.OperationalError: If table 'orders' already created; pass.

    """
    try:
        sql = 'CREATE table orders (name, number, price)'
        conn.execute(sql)
    except sqlite3.OperationalError:
        pass


# CMD FUNCTIONS

def init_produce(conn):
    """Inserts all Produce items in plu_produce.py into the produce.db file.

    All of the items are set to their defaults and so this function should only
    be called upon the first run and to restore item properties to their
    default values.

    Args:
        conn (sqlite3.Connection): Connection to produce.db database file.

    """
    print("THIS WILL SET ALL DATABASE ITEMS TO THEIR DEFAULTS!!!")
    init = input("Continue [y/n]?: ")

    if init[0].lower() == "y":
        for item in plu_produce.produce:
            name = item["name"]
            code = item["code"]
            stock = int(item["stock"])
            price = float(item["price"])

            sql = 'INSERT into produce (name, code, stock, price) ' \
                  'values ("{0}", "{1}", "{2}", "{3}")'
            sql = sql.format(name, code, stock, price)
            conn.execute(sql)
        print("\nSuccessfully initiated Produce database!")


def get_produce(conn, name):
    """Searches for parameter 'name' in table 'produce' in produce.db.

    Args:
        conn (sqlite3.Connection): Connection to produce.db database file.
        name (str): Name of Produce to search for in database.

    Returns:
        list: Contains all results of search.

    """
    sql = 'SELECT * FROM produce WHERE name="{0}"'.format(name.title())
    results = conn.execute(sql)
    produce = results.fetchall()
    return produce


def item_info_name(conn):
    """Searches database for items information and displays it; search by name.

    Args:
        conn (sqlite3.Connection): Connection to produce.db database file.

    """
    name = input("Name of Produce [eg. Carrots (Bunch)]: ")
    produce = get_produce(conn, name)

    for item in produce:
        name, code, stock, price = item
        output = "\nName: {0}\nCode: {1}\nStock: {2}\nPrice: {3}"
        print(output.format(name, code, stock, price))

    if not produce:
        print("\nNo results...")


def item_info_code(conn):
    """Searches database for items information and displays it; search by code.

    Args:
        conn (sqlite3.Connection): Connection to produce.db database file.

    """
    code = input("Code for Produce: ")

    sql = 'SELECT * FROM produce WHERE code="{0}"'.format(code)
    result = conn.execute(sql)
    produce = result.fetchall()

    for item in produce:
        name, code, stock, price = item
        output = "\nName: {0}\nCode: {1}\nStock: {2}\nPrice: {3}"
        print(output.format(name, code, stock, price))

    if not produce:
        print("\nNo results...")


def list_produce(conn):
    """Lists all produce and their attributes in table 'produce' in produce.db.

    Args:
        conn (sqlite3.Connection): Connection to produce.db database file.

    """
    sql = 'SELECT * FROM produce'
    results = conn.execute(sql)
    produce = results.fetchall()

    for item in produce:
        print(item)


def add_produce_stock(conn, name="", number=0):
    """Adds stock to an item in the database.

    Function can be called from order_in(conn) to add items in the order to the
    database.

    Args:
        conn (sqlite3.Connection): Connection to produce.db database file.
        name (str): Name of Produce item.
        number (int): Number of item to be added to items stock.

    Raises:
        ValueError: If 'number' not an integer.

    """
    try:
        if not name:
            name = input("Name of Produce [eg. Carrots (Bunch)]: ")
        if not number:
            number = int(input("Number of {0} to add: ".format(name)))

        produce = get_produce(conn, name)

        for item in produce:
            total = number + int(item[2])
            sql = 'UPDATE produce SET stock="{0}" ' \
                  'WHERE name="{1}" AND stock="{2}"'
            sql = sql.format(total, name.title(), item[2])
            conn.execute(sql)
            print("\nAdded {0} to {1} stock!".format(number, name))
        if not produce:  # If item is not found in database.
            print("\nERROR: '{0}' not found in database!".format(name))
    except ValueError:
        print("\nERROR: Input must be an integer!")


def sub_produce_stock(conn, name="", number=0):
    """Subtracts stock from an item in the database.

    Function can be called from order_out(conn) to subtract items in the order
    from the database.

    Args:
        conn (sqlite3.Connection): Connection to produce.db database file.
        name (str): Name of Produce item.
        number (int): Number of item to be subtracted from items stock.

    Raises:
        ValueError: If 'number' not an integer.

    """
    try:
        if not name:
            name = input("Name of Produce [eg. Carrots (Bunch)]: ")
        if not number:
            number = int(input("Number of {0} to add: ".format(name)))

        produce = get_produce(conn, name)

        for item in produce:
            total = int(item[2]) - number
            sql = 'UPDATE produce SET stock="{0}" ' \
                  'WHERE name="{1}" AND stock="{2}"'
            sql = sql.format(total, name.title(), item[2])
            conn.execute(sql)
            print("\nSubtracted {0} from {1} stock!".format(number, name))
        if not produce:  # If item is not found in database.
            print("\nERROR: '{0}' not found in database!".format(name))
    except ValueError:
        print("\nERROR: Input must be an integer!")


def change_produce_price(conn):
    """Changes an items price in the database.

    Args:
        conn (sqlite3.Connection): Connection to produce.db database file.

    Raises:
        ValueError: If 'number' not a float (or an integer).

    """
    try:
        name = input("Name of Produce [eg. Carrots (Bunch)]: ")
        number = float(input("Change price of {0} to: ".format(name)))
        number = round(number, 2)
        produce = get_produce(conn, name)

        for item in produce:
            sql = 'UPDATE produce SET price="{0}" ' \
                  'WHERE name="{1}" AND price="{2}"'
            sql = sql.format(number, name.title(), item[3])
            conn.execute(sql)
            print("\nUpdated price of {0} to ${1}".format(name, number))
        if not produce:  # If item is not found in database.
            print("\nERROR: '{0}' not found in database!".format(name))
    except ValueError:
        print("\nERROR: Input must be an integer!")


def add_produce_item(conn):
    """Adds a new item to the database.

    Args:
        conn (sqlite3.Connection): Connection to produce.db database file.

    Raises:
        ValueError: If 'stock' is not an integer and/or 'price' is not a float
        (or an integer).

    """
    try:
        name = input("Name of Produce [eg. Carrots (Bunch)]: ")
        code = input("Code for {0}: ".format(name))
        stock = int(input("Number of stock for {}: ".format(name)))
        price = round(float(input("Price for {}".format(name))), 2)

        sql = 'INSERT INTO produce (name, code, stock, price) ' \
              'values ("{0}", "{1}", "{2}", "{3}")'
        sql = sql.format(name, code, stock, price)
        conn.execute(sql)
        print("\nAdded {0} to produce database!".format(name))
    except ValueError:
        print("\nERROR: Input must be an integer!")


def del_produce_item(conn):
    """Deletes an item from the database.

    Args:
        conn (sqlite3.Connection): Connection to produce.db database file.

    Raises:
        ValueError: If 'name' is not a string.

    """
    try:
        name = input("Name of Produce [eg. Carrots (Bunch)]: ")

        sql = 'DELETE FROM produce WHERE name="{}"'.format(name.title())
        conn.execute(sql)
        print("\nDeleted {} from produce database!".format(name))
    except ValueError:
        print("\nERROR: Input must be a string!")


# ORDER FUNCTIONS

def create_order(conn):
    """Creates a list of items to be added to a Produce order 'form'.

    Asks the user if they want to add more produce to the order.

    Args:
        conn (sqlite3.Connection): Connection to produce.db database file.

    Raises:
        ValueError: If 'name' is not a string.

    """
    try:
        name = input("Name of Produce [eg. Carrots (Bunch)]: ")
        number = int(input("Number of {}: ".format(name)))
        price = 0.0

        sql = 'SELECT * FROM produce WHERE name="{}"'.format(name.title())
        result = conn.execute(sql)
        produce = result.fetchall()

        for item in produce:
            name = item[0]
            price = float(item[3])

        sql = 'INSERT INTO orders (name, number, price) ' \
              'values ("{0}", "{1}", "{2}")'
        sql = sql.format(name, number, price)
        conn.execute(sql)
    except ValueError:
        print("\nERROR: Input must be an integer!")

    choice = input("\nOrder another item [y/n]?: ")

    if choice[0].lower() == "y":
        create_order(conn)


def list_order(conn):
    """Displays the items in an already-created order.

    Args:
        conn (sqlite3.Connection): Connection to produce.db database file.

    """
    try:
        sql = 'SELECT * FROM orders'
        result = conn.execute(sql)
        produce = result.fetchall()

        for item in produce:
            print(item)
    except sqlite3.OperationalError:
        print("\nERROR: No order was found!")


def order_in(conn):
    """Adds all items in an already-created order to the database.

    Args:
        conn (sqlite3.Connection): Connection to produce.db database file.

    Raises:
        sqlite3.OperationalError: If database entry did not work.

    """
    total = 0.0

    try:
        sql = 'SELECT * FROM orders'
        result = conn.execute(sql)
        order = result.fetchall()

        for item in order:
            add_produce_stock(conn, name=item[0], number=int(item[1]))
            total += float(item[2])

        if order:
            print("Total for order: ${}".format(round(total, 2)))
    except sqlite3.OperationalError:
        print("ERROR: Could not complete order in!")


def order_out(conn):
    """Subtracts all items in an already-created order from the database.

    Args:
        conn (sqlite3.Connection): Connection to produce.db database file.

    Raises:
        sqlite3.OperationalError: If database entry did not work.

    """
    total = 0.0

    try:
        sql = 'SELECT * FROM orders'
        result = conn.execute(sql)
        order = result.fetchall()

        for item in order:
            sub_produce_stock(conn, name=item[0], number=int(item[1]))
            total += float(item[2])
        if order:
            print("Total for order: ${}".format(round(total, 2)))
    except sqlite3.OperationalError:
        print("ERROR: Could not complete order in!")


def drop_table_orders(conn):
    """Deletes the table 'orders' and thus deletes the Produce order 'form'.

    Args:
        conn (sqlite3.Connection): Connection to produce.db database file.

    """
    sql = 'DROP table orders'
    conn.execute(sql)
    print("\nDeleted order!")
