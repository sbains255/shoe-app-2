import datetime
import sqlite3

from kivy import Logger
from kivy.event import EventDispatcher


class SQLiteDataBase(EventDispatcher):
    data_base_path = 'db/database.db'
    db = None
    cursor = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # load database
        self.db = sqlite3.connect(self.data_base_path)
        self.cursor = self.db.cursor()

    def add_product(self, size, name, image_ext, product_id):
        Logger.info('Database: Save product to database')

        # command to  create table and fields
        comm1 = f'CREATE TABLE IF NOT EXISTS products ( product_id TEXT  PRIMARY KEY, size  INTEGER,image_ext TEXT ,' \
                f'product_name TEXT)'
        self.cursor.execute(comm1)
        comm2 = f"INSERT INTO products VALUES  ( '{product_id}','{size}','{image_ext}','{name}')"

        self.cursor.execute(comm2)
        # commit changes (save database)
        self.db.commit()

    def load_products(self):
        Logger.info('Database: load products from database')

        self.cursor.execute(f" SELECT count(name) FROM sqlite_master WHERE type='table' AND name='products' ")

        if self.cursor.fetchone()[0] == 1:
            # load data from table
            self.cursor.execute(f'SELECT * FROM "products"')
            data = self.cursor.fetchall()
            return data
        else:
            return None

    def load_customers(self):
        Logger.info('Database: load customers from database')

        self.cursor.execute(f" SELECT count(name) FROM sqlite_master WHERE type='table' AND name='customers' ")

        if self.cursor.fetchone()[0] == 1:
            # load data from table
            self.cursor.execute(f'SELECT * FROM "customers"')
            data = self.cursor.fetchall()
            return data
        else:
            return None

    def customer_sign_up(self, customer_id, password):
        try:
            Logger.info('Database: Create customer account')
            # command to  create table and fields
            comm1 = f'CREATE TABLE IF NOT EXISTS customers (user_id TEXT  PRIMARY KEY, password TEXT)'
            self.cursor.execute(comm1)
            comm2 = f"INSERT INTO customers VALUES  ( '{customer_id}','{password}')"
            self.cursor.execute(comm2)
            # commit changes (save database)
            self.db.commit()
            return True
        except:
            return False

    def add_product_to_customer_cart(self, customer_id, product_id):
        order_date = str(datetime.datetime.now().strftime("%d%m%Y%H%M%S"))
        # command to  create table and fields
        comm1 = f"CREATE TABLE IF NOT EXISTS '{customer_id}' (order_date TEXT  PRIMARY KEY, product_id TEXT)"
        self.cursor.execute(comm1)
        comm2 = f"INSERT INTO '{customer_id}' VALUES  ( '{order_date}','{product_id}')"
        self.cursor.execute(comm2)
        # commit changes (save database)
        self.db.commit()

    def remove_product_from_customer_cart(self, customer_id, order_date):

        # command to  create table and fields
        comm1 = f"CREATE TABLE IF NOT EXISTS '{customer_id}' (order_date TEXT  PRIMARY KEY, product_id TEXT)"

        comm2 = f"DELETE from '{customer_id}' where order_date = '{order_date}'"
        self.cursor.execute(comm1)
        self.cursor.execute(comm2)
        self.db.commit()

    def get_customer_cart_products(self, customer_id):

        self.cursor.execute(f" SELECT count(name) FROM sqlite_master WHERE type='table' AND name='{customer_id}' ")

        if self.cursor.fetchone()[0] == 1:
            # load data from table
            self.cursor.execute(f'SELECT * FROM "{customer_id}"')
            data = self.cursor.fetchall()
            return data
        else:
            return None
