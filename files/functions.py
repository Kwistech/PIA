import sqlite3
from files import plu_produce


# MENUS

def menu():
    welcome = "Welcome to your Produce Inventory Assistant, PIA!"
    more_info = "Type 'help' for more info."
    line = "-" * len(welcome)
    spacer = "\n"
    print(spacer)
    print(line)
    print(welcome)
    print(more_info)


def help_menu():
    f = open("./files/help.txt")
    lines = f.readlines()

    for line in lines:
        print(line.strip())


def pia():
    f = open('README.md')
    lines = f.readlines()

    for line in lines:
        print(line.strip())


# INITIALIZING FUNCTIONS

def connect_db():
    conn = sqlite3.connect("./files/produce.db")
    return conn


def cursor_db(conn):
    cursor = conn.cursor()
    return cursor


def create_table_produce(conn):
    try:
        sql = 'create table produce (name, code, stock, price)'
        conn.execute(sql)
    except sqlite3.OperationalError:
        pass


def create_table_order(conn):
    try:
        sql = 'create table orders (name, number, price)'
        conn.execute(sql)
    except sqlite3.OperationalError:
        pass


# CMD FUNCTIONS

def init_produce(conn):
    print("THIS WILL SET ALL DATABASE ITEMS TO THEIR DEFAULTS!!!")
    init = input("Continue [y/n]?: ")

    if init[0].lower() == "y":
        for item in plu_produce.produce:
            name = item["name"]
            code = item["code"]
            stock = int(item["stock"])
            price = float(item["price"])

            sql = 'insert into produce (name, code, stock, price) values ("{0}", "{1}", "{2}", "{3}")'
            sql = sql.format(name, code, stock, price)
            conn.execute(sql)
        print("\nSuccessfully initiated Produce database!")


def get_produce(conn, name):
    sql = 'select * from produce where name="{0}"'.format(name.title())
    results = conn.execute(sql)
    produce = results.fetchall()
    return produce


def item_info_name(conn):
    name = input("Name of Produce [eg. Carrots (Bunch)]: ")
    produce = get_produce(conn, name)

    for item in produce:
        name, code, stock, price = item
        output = "\nName: {0}\nCode: {1}\nStock: {2}\nPrice: {3}"
        print(output.format(name, code, stock, price))

    if not produce:
        print("\nNo results...")


def item_info_code(conn):
    code = input("Code for Produce: ")

    sql = 'select * from produce where code="{0}"'.format(code)
    result = conn.execute(sql)
    produce = result.fetchall()

    for item in produce:
        name, code, stock, price = item
        output = "\nName: {0}\nCode: {1}\nStock: {2}\nPrice: {3}"
        print(output.format(name, code, stock, price))

    if not produce:
        print("\nNo results...")


def list_produce(conn):
    sql = 'select * from produce'
    results = conn.execute(sql)
    produce = results.fetchall()

    for item in produce:
        print(item)


def add_produce_stock(conn, name="", number=0):
    try:
        if not name:
            name = input("Name of Produce [eg. Carrots (Bunch)]: ")
        if not number:
            number = int(input("Number of {0} to add: ".format(name)))

        produce = get_produce(conn, name)

        for item in produce:
            total = number + int(item[2])
            sql = 'update produce set stock="{0}" where name="{1}" and stock="{2}"'
            sql = sql.format(total, name.title(), item[2])
            conn.execute(sql)
            print("\nAdded {0} to {1} stock!".format(number, name))
        if not produce:
            print("\nERROR: '{0}' not found in database!".format(name))
    except ValueError:
        print("\nERROR: Input must be an integer!")


def sub_produce_stock(conn, name="", number=0):
    try:
        if not name:
            name = input("Name of Produce [eg. Carrots (Bunch)]: ")
        if not number:
            number = int(input("Number of {0} to add: ".format(name)))

        produce = get_produce(conn, name)

        for item in produce:
            total = int(item[2]) - number
            sql = 'update produce set stock="{0}" where name="{1}" and stock="{2}"'
            sql = sql.format(total, name.title(), item[2])
            conn.execute(sql)
            print("\nSubtracted {0} from {1} stock!".format(number, name))
        if not produce:
            print("\nERROR: '{0}' not found in database!".format(name))
    except ValueError:
        print("\nERROR: Input must be an integer!")


def change_produce_price(conn):
    try:
        name = input("Name of Produce [eg. Carrots (Bunch)]: ")
        number = round(float(input("Change price of {0} to: ".format(name))), 2)
        produce = get_produce(conn, name)

        for item in produce:
            sql = 'update produce set price="{0}" where name="{1}" and price="{2}"'
            sql = sql.format(number, name.title(), item[3])
            conn.execute(sql)
            print("\nUpdated price of {0} to ${1}".format(name, number))
        if not produce:
            print("\nERROR: '{0}' not found in database!".format(name))
    except ValueError:
        print("\nERROR: Input must be an integer!")


def add_produce_item(conn):
    try:
        name = input("Name of Produce [eg. Carrots (Bunch)]: ")
        code = input("Code for {0}: ".format(name))
        stock = int(input("Number of stock for {}: ".format(name)))
        price = round(float(input("Price for {}".format(name))), 2)

        sql = 'insert into produce (name, code, stock, price) values ("{0}", "{1}", "{2}", "{3}")'
        sql = sql.format(name, code, stock, price)
        conn.execute(sql)
        print("\nAdded {0} to produce database!".format(name))
    except ValueError:
        print("\nERROR: Input must be an integer!")


def del_produce_item(conn):
    try:
        name = input("Name of Produce [eg. Carrots (Bunch)]: ")

        sql = 'delete from produce where name="{}"'.format(name.title())
        conn.execute(sql)
        print("\nDeleted {} from produce database!".format(name))
    except ValueError:
        print("\nERROR: Input must be a string!")


# ORDER FUNCTIONS

def create_order(conn):
    try:
        name = input("Name of Produce [eg. Carrots (Bunch)]: ")
        number = int(input("Number of {}: ".format(name)))
        price = 0.0

        sql = 'select * from produce where name="{}"'.format(name.title())
        result = conn.execute(sql)
        produce = result.fetchall()

        for item in produce:
            name = item[0]
            price = float(item[3])

        sql = 'insert into orders (name, number, price) values ("{0}", "{1}", "{2}")'
        sql = sql.format(name, number, price)
        conn.execute(sql)
    except ValueError:
        print("\nERROR: Input must be an integer!")

    choice = input("\nOrder another item [y/n]?: ")

    if choice[0].lower() == "y":
        create_order(conn)


def display_order(conn):
    sql = 'select * from orders'
    result = conn.execute(sql)
    produce = result.fetchall()

    for item in produce:
        print(item)


def order_in(conn):
    total = 0.0

    try:
        sql = 'select * from orders'
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
    total = 0.0

    try:
        sql = 'select * from orders'
        result = conn.execute(sql)
        order = result.fetchall()

        for item in order:
            sub_produce_stock(conn, name=item[0], number=int(item[1]))
            total += float(item[2])
        if order:
            print("Total for order: ${}".format(round(total, 2)))
    except sqlite3.OperationalError:
        print("ERROR: Could not complete order in!")
