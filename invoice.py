import logging

import tabulate
from file_Handler import FileHandler
from functions import list_parser


class Invoice:
    invoice_file = FileHandler("invoices.csv")


    @staticmethod
    def print_pre_invoices(product_list):
        print("----------------------------Pre invoices-------------------------")
        header = product_list[0].keys()
        rows = [x.values() for x in product_list]
        print(tabulate.tabulate(rows, header, tablefmt='grid'))
        print("sum of product")
        print(Invoice.calculate_total(product_list))

    @staticmethod
    def calculate_total(product_list):
        total = sum([i['price']*i['number_of_product'] for i in product_list])
        return total

    def edit_invoices(self, username, invoices):
        invoice_list = self.invoice_file.read_file()
        customer_info = None
        final_invoices = []
        check_username = False
        for i in invoice_list:
            if i["username"] == username:
                check_username = True
                customer_info = i
            else:
                final_invoices.append(i)

        if check_username:
            info_invoice = self.edit_row(username, customer_info, invoices)
            final_invoices.append(info_invoice)
            self.invoice_file.edit_to_file(final_invoices)
        else:
            self.add_invoices(username, invoices)

    def add_invoices(self, username, invoicse):
        self.invoice_file.add_to_file({"username" : username,"invoices" : invoicse})

    def edit_row(self,username, customer_info, invoices):
        list_invoices = list_parser(customer_info["invoices"])
        for i in invoices:
            list_invoices.append(i)
        row = {"username" : username, "invoices": list_invoices}
        return row

    def show_customer_invoices(self, username):
        info_username = self.invoice_file.find_row_item("username", username)
        if info_username:
            list_invoices = list_parser(info_username["invoices"])
            self.print_invoices_customer(list_invoices)
        else:
            print("there is not any invoices first buy from shop")
            logging.info("there is not any invoices first buy from shop")


    @staticmethod
    def print_invoices_customer(list_invoices):
        header = list_invoices[0].keys()
        rows = [x.values() for x in list_invoices]
        print(tabulate.tabulate(rows, header, tablefmt='grid'))

    def view_all_customer_invoices(self, store_name):
        reader = self.invoice_file.read_file()
        check_store_name = False
        final_list=[]
        for i in reader:
            list_invoices = list_parser(i['invoices'])
            for invoice in list_invoices:
                product_list = invoice["products"]
                for product in product_list:
                    if product['store_name'] == store_name:
                        check_store_name = True
                if check_store_name:
                    final_list.append({"username":i["username"],'invoice':invoice})

        if final_list:
            self.print_invoices_customer(final_list)
        else:
            print(f"No customer has purchased from {store_name} store")
            logging.info(f"No customer has purchased from {store_name} store")









