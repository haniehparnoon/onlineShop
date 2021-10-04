from file_Handler import FileHandler
from functions import list_parser
import logging
import tabulate
import datetime

class Store:
    store_file = FileHandler("Stores.csv")

    def __init__(self, username, store_name, open_time, close_time, products=None, block_list=None):
        self.username = username
        self.store_name = store_name
        self.open_time = open_time
        self.close_time = close_time
        self.products = products
        self.block_list = block_list
        if not (self.store_file.find_row_item("username", self.username)):
            self.store_file.add_to_file(self.__dict__)
            logging.info("new store Added")

    def add_product(self, new_product_list):
        update_file_list = []
        row = self.store_file.find_row_item('username', self.username)
        if row["products"] == '':
            self.products = new_product_list
        else:
            previous_product = list_parser(row['products'])
            for i in previous_product:
                new_product_list.append(i)
                self.products = new_product_list

        update_file_list.append(self.__dict__)
        for i in self.read_file():
            if i['username'] != self.username:
                update_file_list.append(i)

        self.store_file.edit_to_file(update_file_list)
        logging.info("new products added")

    def view_inventory(self):
        list_products = self.find_product_in_store_file()
        inventory = [product for product in list_products if product['number_available'] != 0]
        return inventory

    def finished_products(self):
        list_products = self.find_product_in_store_file()
        if list_products:
            finished_product = [product for product in list_products if product['number_available'] <= 1]
            logging.info("finish product")
            return finished_product

    @staticmethod
    def view_product(list_product):
        if list_product:
            header = list_product[0].keys()
            rows = [x.values() for x in list_product]
            print(tabulate.tabulate(rows, header, tablefmt='grid'))

    def block_customer_from_store(self, new_block_customer):
        update_file_list = []
        row = self.store_file.find_row_item('username', self.username)
        if row["block_list"] == '':
            self.block_list = [new_block_customer]
        else:
            previous_block_list = list_parser(row['block_list'])
            if new_block_customer not in previous_block_list:
                previous_block_list.append(new_block_customer)
                self.block_list = previous_block_list
            else:
                print("this user exist in block list")

        update_file_list.append(self.__dict__)
        for i in self.read_file():
            if i['username'] != self.username:
                update_file_list.append(i)

        self.store_file.edit_to_file(update_file_list)
        logging.info("block user")

    def read_file(self):
        reader = self.store_file.read_file()
        #print(reader)
        return reader

    def find_product_in_store_file(self):
        store_product_info = self.store_file.find_row_item('username', self.username)
        if store_product_info['products']:
            list_products = list_parser(store_product_info['products'])
            return list_products

    # if customer in block list return True
    def check_customer(self, username):
        if self.block_list != '':
            block_list = list_parser(self.block_list)
            if username in block_list:
                return True
            else:
                return False
        else:
            return False

    # if product that user choose is available return that
    def check_available_choose_product(self, data):
        product_store_list = list_parser(self.products)
        for i in product_store_list:
            if data['product_name'] == i['product_name']:
                if data["number_of_product"] <= i["number_available"]:
                    return {'store_name': data["store_name"], "product_name": i["product_name"],
                            'price': i['price'], "number_of_product": data["number_of_product"]}

    def update_product(self, product_name, number_of_product):
        reader = self.read_file()
        final_list = []
        product_list = []

        for i in reader:
            if i["store_name"] != self.store_name:
                final_list.append(i)
            elif i['store_name'] == self.store_name:
                list_product = list_parser(i["products"])
                for product in list_product:
                    if product["product_name"] == product_name:
                        if product["number_available"] >= number_of_product:
                            new_available_number = product["number_available"] - number_of_product
                            product["number_available"] = new_available_number
                            product_list.append(product)
                    else:
                        product_list.append(product)
        print(product_list)
        self.products = product_list
        # self.block_customer =
        final_list.append(self.__dict__)
        self.store_file.edit_to_file(final_list)











