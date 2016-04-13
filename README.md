#Produce Inventory Assistant (PIA) 

Produce Inventory Assistant (PIA) v.1.0

Produce Inventory Assistant (PIA) makes inventory management simple! PIA is an easy-to-use program which helps small
grocery stores manage their in-store Produce inventory and information.

PIA is recommended for grocery store owners who want a fast and simple alternative to other inventory management
programs.

Check the project's [Wiki](https://github.com/Kwistech/PIA/wiki) for more info.

##Installation

This program is not installed. It is run from the command line.

Fork the repository and clone it to your local drive.

From the program's root directory, run the following:

`python main.py`

##Upon First Run##

The items in the plu_produce.py need to be added to the produce.db database.

To do this, type 'init' and then confirm with 'y':

```
-------------------------------------------------
Welcome to your Produce Inventory Assistant, PIA!
Type 'help' for more info.
> init
THIS WILL SET ALL DATABASE ITEMS TO THEIR DEFAULTS!!!
Continue [y/n]?: y
```

**Note: Only do this once as this will add all Produce items to the database with their default values!**

##Features

With PIA, one can:
+ Add/Subtract Produce to/from the inventory database
+ Add/Subtract items in an order to/from the inventory database
+ Add/Delete items from the inventory database
+ Search for produce information via name or PLU code
+ Create an incoming or an outgoing order
+ Change an item's price

##Menu Commands

Below are the basic commands for the program 

More info can be found in ./files/help.txt:

+ help
+ pia
+ init
+ info name
+ info code
+ list
+ in
+ out
+ price
+ add item
+ del item
+ create order
+ list order
+ order in
+ order out
+ del order
+ quit
