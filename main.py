# PIA (Produce Inventory Assistant) - Johnathon Kwisses (Kwistech)

from files import functions


def main():
    conn = functions.connect_db()
    functions.cursor_db(conn)
    functions.create_table_produce(conn)
    functions.create_table_order(conn)

    while True:
        functions.menu()
        cmd = input("> ").lower()

        if cmd[0] == "q":
            break
        elif cmd == "help":
            functions.help_menu()
        elif cmd == "pia":
            functions.pia()
        elif cmd == "init":
            functions.init_produce(conn)

        elif cmd == "info name":
            functions.item_info_name(conn)
        elif cmd == "info code":
            functions.item_info_code(conn)
        elif cmd == "list":
            functions.list_produce(conn)

        elif cmd == "in":
            functions.add_produce_stock(conn)
        elif cmd == "out":
            functions.sub_produce_stock(conn)
        elif cmd == "price":
            functions.change_produce_price(conn)

        elif cmd == "add item":
            functions.add_produce_item(conn)
        elif cmd == "del item":
            functions.del_produce_item(conn)

        elif cmd == "create order":
            functions.create_order(conn)
        elif cmd == "display order":
            functions.display_order(conn)
        elif cmd == "order in":
            functions.order_in(conn)
        elif cmd == "order out":
            functions.order_out(conn)

        # conn.commit()

    conn.close()

if __name__ == "__main__":
    main()
