import sqlite3
from files import plu_produce


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
    f = open("help.txt")
    lines = f.readlines()

    for line in lines:
        print(line.strip())


def pia():
    # Need to fix. Open README.md, but it is in parent directory.
    f = open('C:\\Users\John\Documents\GitHub\PIA\README.md')
    lines = f.readlines()

    for line in lines:
        print(line.strip())


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
    # Problem code...maybe can't create multiple tables in a db?
    try:
        sql = 'create table order (name, number, price)'
        conn.execute(sql)
    except sqlite3.OperationalError:
        print("ERROR")


def init_produce(conn):
    warning = "THIS WILL SET ALL DATABASE ITEMS TO THEIR DEFAULTS!!!"
    print(warning)
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


def item_info_name(conn):
    name = input("Name of Produce [eg. Carrots (Bunch)]: ")

    try:
        produce = get_produce(conn, name)

        for item in produce:
            name, code, stock, price = item
            output = "\nName: {}\nCode: {}\nStock: {}\nPrice: {}"
            print(output.format(name, code, stock, price))
    except:
        print("ERRORSSSS")


def item_info_code(conn):
    code = input("Code for Produce: ")

    try:
        sql = 'select * from produce where code="{0}"'.format(code)
        result = conn.execute(sql)
        produce = result.fetchall()

        for item in produce:
            name, code, stock, price = item
            output = "\nName: {}\nCode: {}\nStock: {}\nPrice: {}"
            print(output.format(name, code, stock, price))
    except:
        print("ERRORSSSS")


def list_produce(conn):
    sql = 'select * from produce'
    results = conn.execute(sql)
    produce = results.fetchall()

    for item in produce:
        print(item)


def get_produce(conn, name):
    sql = 'select * from produce where name="{0}"'.format(name.title())
    results = conn.execute(sql)
    produce = results.fetchall()
    return produce


def add_produce_stock(conn):
    name = input("Name of Produce [eg. Carrots (Bunch)]: ")
    number = int(input("Number of {0} to add: ".format(name)))

    try:
        produce = get_produce(conn, name)

        for item in produce:
            total = number + int(item[2])
            sql = 'update produce set stock="{0}" where name="{1}" and stock="{2}"'
            sql = sql.format(total, name.title(), item[2])
            conn.execute(sql)
            print("\nAdded {} to {} stock!".format(number, name))
        else:
            if not produce:
                print("No item!")  # Replace with better error handling function calls.
    except ValueError:
        print("ERROR!")


def sub_produce_stock(conn):
    name = input("Name of Produce [eg. Carrots (Bunch)]: ")
    number = int(input("Number of {0} to subtract: ".format(name)))

    try:
        produce = get_produce(conn, name)

        for item in produce:
            total = int(item[2]) - number
            sql = 'update produce set stock="{0}" where name="{1}" and stock="{2}"'
            sql = sql.format(total, name.title(), item[2])
            conn.execute(sql)
            print("\nSubtracted {} from {} stock!".format(number, name))
        else:
            if not produce:
                print("No item!")  # Replace with better error handling function calls.
    except ValueError:
        print("ERROR!")


def change_produce_price(conn):
    name = input("Name of Produce [eg. Carrots (Bunch)]: ")
    number = round(float(input("Change price of {} to: ".format(name))), 2)

    try:
        produce = get_produce(conn, name)

        for item in produce:
            sql = 'update produce set price="{0}" where name="{1}" and price="{2}"'
            sql = sql.format(number, name.title(), item[3])
            conn.execute(sql)
            print("\nUpdated price of {0} to ${1}".format(name, number))  # round!
        else:
            if not produce:
                print("No item!")  # Replace with better error handling function calls.
    except ValueError:
        print("ERROR!")


def add_produce_item(conn):
    name = input("Name of Produce [eg. Carrots (Bunch)]: ")
    code = input("Code for {}: ".format(name))
    stock = int(input("Number of stock for {}: ".format(name)))
    price = round(float(input("Price for {}".format(name))), 2)

    try:
        sql = 'insert into produce (name, code, stock, price) values ("{0}", "{1}", "{2}", "{3}")'
        sql = sql.format(name, code, stock, price)
        conn.execute(sql)
        print("\nAdded {} to produce database!".format(name))
    except:
        print("ERROR: Something happened!")


def del_produce_item(conn):
    name = input("Name of Produce [eg. Carrots (Bunch)]: ")

    try:
        sql = 'delete from produce where name="{}"'.format(name.title())
        conn.execute(sql)
        print("\nDeleted {} from produce database!".format(name))
    except:
        print("ERROR: Something happened!")


def produce_order(conn):
    # Need to fix! Errors everywhere!
    order = []

    while True:
        name = input("Name of Produce [eg. Carrots (Bunch)]: ")

        if name == "q":
            break

        number = int(input("Number of {}: ".format(name)))

        try:
            sql = 'select * from produce where name="{}"'.format(name.title())
            result = conn.execute(sql)
            produce = result.fetchall()

            for item in produce:
                name = item[0]
                price = float(item[3])

                sql = 'insert into order (name, number, price) values ("{0}", {1}, {2})'
                sql = sql.format(name, number, price)
                conn.execute(sql)
        except:
            print("ERROR: produce_order 1")

        try:
            sql = 'select * from order'
            result = conn.execute(sql)
            produce = result.fetchall()

            for item in produce:
                print(item)
        except:
            print("ERROR: 5")

    print(order)
