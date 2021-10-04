import logging

import functions
from users import User
import datetime
from store import Store
from file_Handler import FileHandler
import tabulate
from invoice import Invoice


class Customer(User):
    stores_file = FileHandler("Stores.csv")
    final_factors=[]

    @classmethod
    def print_menu_access(cls):
        super().print_menu_access()
        print("----------------------------------Store Manage Menu-------------------------------")
        print("1.View previous invoices\n2.View list of stores\n3.Store Search\n4.Select a store\n"
              "5.View product list\n6.sign out")

    def access_customer(self):
        n = 11
        while n != 6:
            self.print_menu_access()
            n = int(input("choose number access"))
            if n == 1:
                self.view_previous_invoices()
            elif n == 2:
                self.view_list_of_stores()
            elif n == 3:
                self.store_search()
            elif n == 4:
                self.select_store()
            elif n == 5:
                self.view_product_list()
            # elif n == 6:
            #     self.product_search()
            #elif n == 7:
                #self.select_products()
            # elif n == 8:
            #     self.view_pre_invoice()
            # elif n == 9:
            #     self.confirm_product_or_edit()
            elif n == 6:
                print("you logged out")
                self.sign_out()
                break

    def view_previous_invoices(self):
        invoice = Invoice()
        invoice.show_customer_invoices(self.username)

    def view_list_of_stores(self, store_name = None):
        time_ = self.get_now_time()
        reader = self.stores_file.read_file()
        open_list_store = [i['store_name'] for i in reader
                           if (self.convert_string_to_time(i["open_time"]) <= time_ <= self.convert_string_to_time(i["close_time"]))]
        if not store_name:
            self.print_store([open_list_store])
        return open_list_store

    def store_search(self, store_name = None):
        #store_name = input("enter store name").lower()
        self.select_products(store_name)

    def select_store(self,store_name = None):
        reader = self.stores_file.read_file()
        if store_name:
            list_store = self.view_list_of_stores(store_name)
        else:
            list_store = self.view_list_of_stores()
        if list_store:
            input_store_name = input("enter store name").lower()
            if input_store_name in list_store:
                for i in reader:
                    if i["store_name"] == input_store_name:
                        return i
            else:
                print("there is not this store")
        print("sorry all stores are closed")

    def view_product_list(self, store_name = None):
        if store_name:
            store_info = self.select_store(store_name)
        else:
            store_info = self.select_store()

        if store_info:
            store1 = Store(store_info['username'], store_info['store_name'], store_info['open_time'],
                           store_info['close_time'], store_info['products'], store_info['block_list'])
            if store_info['products'] != '':
                Store.view_product(functions.list_parser(store_info['products']))

            return store1


    def product_search(self):
        pass

    def select_products(self, store_name = None):
        product_list = []
        if store_name:
            store1 = self.view_product_list(store_name)
        else:
            store1 = self.view_product_list()
        if store1:
            check_customer = store1.check_customer(self.username)
            if store1.products != '':
                if not check_customer:
                    input_continue = 'y'
                    while input_continue != 'n':
                        input_continue = input("enter y/n (y to continue or n to finish").lower()
                        if input_continue == 'n':
                            break
                        else:
                            product_name = input("enter product name").lower()
                            number_of_product = int(input("enter number of product"))
                            data = {'store_name': store1.store_name, "product_name": product_name,
                                    "number_of_product": number_of_product}
                            check_data = store1.check_available_choose_product(data)
                            if check_data:
                                product_list.append(check_data)
                            else:
                                print("product name or number of product is wrong")
                                logging.info("product name or number of product is wrong")
                    self.view_pre_invoice(product_list)
                    list_save_product =self.confirm_product_or_edit(product_list)
                    #final_list = self.confirm_product_or_edit(product_list)
                    # print(final_list)
                    if list_save_product:
                        for product in list_save_product:
                            print(product)
                            store1.update_product(product["product_name"], product["number_of_product"])

                else:
                    print("Sorry you are block you cant select product")
                    logging.info(f"{self.username}  is block cant select product")
            else:
                print("no product list to add")

    def view_pre_invoice(self, pre_invoice):
        Invoice.print_pre_invoices(pre_invoice)

    def confirm_product_or_edit(self, product_list):
        confirm_input = input("enter c to confirm Or d to delete")
        if confirm_input == 'c':
            self.final_factors.append({"products": product_list,"total": Invoice.calculate_total(product_list)})
            logging.info("new invoice added")
            #---------
            # print(self.final_factors)
            # print(product_list)
            return product_list

        elif confirm_input == 'd':
            final_list = []
            while True:
                input_continue = input("Enter y/n y for continue or n to stop")
                if input_continue == 'n':
                    break
                else:
                    product_name_delete = input("Enter name of product that you want delete")
                    final_list = self.delete_product_from_choose_product(product_name_delete, product_list)
            if final_list:
                self.final_factors.append({"products": final_list, "total": Invoice.calculate_total(product_list)})
                logging.info("new invoice added")
            #     #------------
            #     #print(self.final_factors)
            #     print(f"{final_list}final_list")
                return final_list
            else:
                print("there is not any item")

    def sign_out(self):
        invoice = Invoice()
        invoice.edit_invoices(self.username, self.final_factors)


    @staticmethod
    def delete_product_from_choose_product(product_name,list_product):
        list_final = [i for i in list_product if i["product_name"] != product_name]
        return list_final




    @staticmethod
    def convert_string_to_time(time_):
        convert_time = datetime.time(*map(int, time_.split(':')))
        return convert_time

    @staticmethod
    def print_store(list_store):
        print("Stores Name")
        print(tabulate.tabulate(list_store, tablefmt='grid'))

    @staticmethod
    def get_now_time():
        now = datetime.datetime.now()
        time_ = datetime.time(now.hour, now.minute)
        return time_











customer = Customer("09125802238",'0912')
# customer.store_search()
# customer.sign_out()
customer.view_previous_invoices()