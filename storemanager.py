from users import User
from file_Handler import FileHandler
import logging
from functions import hash_password ,list_parser
from store import Store
from datetime import datetime
import tabulate
from invoice import Invoice


class StoreManager(User):
    store_file = FileHandler("Stores.csv")
    users_file = FileHandler('users.csv')

    def __init__(self, username, password):
        super().__init__(username, password)
        self.store = self.find_store()

    @classmethod
    def register_user(cls):
        username = cls.validate_username(input("enter username(phone_number)"))
        password = cls.validate_password(input("enter your password"), input("enter repeat password"))
        h_password = hash_password(password)
        store_name = input("enter store name")
        open_time = cls.chek_format_time(input("enter open time (00:00) "))
        close_time = cls.chek_format_time(input("enter close time (00:00)"))
        if not (cls.users_file.find_row_item('username', username)):
            user_dict = {"type": cls.__name__, "username": username, "password": h_password}
            cls.users_file.add_to_file(user_dict)
            Store(username, store_name, open_time, close_time)
            logging.info("new User Added")
        else:
            print("username Exist")

    @classmethod
    def print_menu_access(cls):
        super().print_menu_access()
        print("----------------------------------Store Manage Menu-------------------------------")
        print("1.Add Product List\n2.View inventory\n3.alarm\n4.View invoices\n"
              "5.Search invoices\n6.View customer information\n7.Block Customer\n8.exit")

    def access_manager(self):
        self.alarm()
        n = 10
        while n != 8:
            self.print_menu_access()
            n = int(input("choose number access"))
            if n == 1:
                self.add_product()
            elif n == 2:
                self.view_remaining_inventory()
            elif n == 3:
                self.alarm()
            elif n == 4:
                self.view_invoices()
            elif n == 5:
                self.search_invoices()
            elif n == 6:
                self.view_information_all_customer()
            elif n == 7:
                self.block_customer()
            elif n == 8:
                self.sign_out()
                break

    def add_product(self):
        product_list = []
        number_product = int(input("Enter number of product you want add "))
        for i in range(number_product):
            print(f"product [{i}]")
            product_name = input("Enter product name")
            barcode = input(" Enter Barcode")
            price = self.validate_price(int(input(" Enter price")))
            brand = input("Enter Brand")
            number_available = int(input("Enter number of product"))
            expire_date = self.validate_expire_date(input(" Enter expire Date(00-03-04)"))
            product_list.append({"product_name": product_name, "barcode": barcode, "price": price, "brand": brand,
                                 "number_available": number_available, "expire_date": expire_date})
        self.store.add_product(product_list)

    def view_remaining_inventory(self):
        self.alarm()
        print('----------------------------------------Available List------------------------------------')
        available_list = self.store.view_inventory()
        self.store.view_product(available_list)

    def alarm(self):
        finished_product = self.store.finished_products()
        if finished_product:
            print('----------------------------------------Alarm List------------------------------------')
            self.store.view_product(finished_product)
        else:
            print("*****no item in alarm list****")
            logging.info("*****no item in alarm list****")

    def view_invoices(self):
        invoices = Invoice()
        invoices.view_all_customer_invoices(self.store.store_name)

    def view_information_all_customer(self):
        self.print_customer(self.find_customers())

    def block_customer(self):
        customer_list = self.find_customers()
        self.print_customer(customer_list)
        choose_username = StoreManager.validate_username(input("enter username that you want block"))
        if choose_username in customer_list:
            self.store.block_customer_from_store(choose_username)
        else:
            print("this username dos not exist you can not block")
            logging.info("this username dos not exist you can not block")

    def search_invoices(self):
        pass

    def sign_out(self):
        print("Bye sign out")

    def find_store(self):
        file_store = self.store_file.find_row_item("username", self.username)
        return Store(file_store['username'], file_store['store_name'], file_store['open_time'], file_store['close_time']
                     , file_store['products'], file_store['block_list'])

    @staticmethod
    def validate_expire_date(date):
        try:
            datetime.strptime(date, '%y-%m-%d')
            return date
        except ValueError as v:
            print(f"format date is wrong{v}")
            logging.info(f"format date is wrong{v}")

    @staticmethod
    def validate_price(price):
        try:
            if isinstance(price, int) or isinstance(price, float):
                return price
        except ValueError as v:
            print(f"{v} price should be int or float ")
            logging.info(f"{v} price should be int or float")

    def find_customers(self):
        users_list = self.users_file.read_file()
        customer_list = [user["username"] for user in users_list if user['type'] == 'Customer']
        return customer_list

    @staticmethod
    def print_customer(customer_list):
        print("Customers")
        print(tabulate.tabulate([customer_list], tablefmt='grid'))


















