from users import User
from customer import Customer
from storemanager import StoreManager
import logging

logging.basicConfig(filename='app.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
def show_menu():
    choice = 1
    while choice != 3:
        print(
            "-----------------------------------MAIN MENU-----------------------------------------")
        print("1.Register\n2.Sign in\n3.Log out")
        choice = int(input("Enter Number (Main Menu)"))
        if choice == 1:
            print("1.store manager\n2.Customer")
            role_selection = int(input("Enter number of your role"))
            if role_selection == 1:
                StoreManager.register_user()
            elif role_selection == 2:
                Customer.register_user()
            else:
                raise Exception("invalid input ")
        elif choice == 2:
            user_info = User.login_user()
            if user_info:
                if user_info["type"] == "StoreManager":
                    storemanager1 = StoreManager(user_info["username"],user_info["password"])
                    storemanager1.access_manager()
                elif user_info['type'] == "Customer":
                    customer = Customer(user_info["username"],user_info["password"])
                    customer.access_customer()
            else:
                print("username or password was wrong")
                logging.info("unsuccessful log in")

        else:
            break


show_menu()



