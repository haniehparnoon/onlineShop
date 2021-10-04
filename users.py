import logging
import ast
import datetime
from file_Handler import FileHandler
from functions import hash_password, list_parser


class User:
    users_file = FileHandler("users.csv")
    def __init__(self,username, password):
        self.username = username
        self.password = password

    @classmethod
    def register_user(cls):
        username = cls.validate_username(input("enter username(phone_number)"))
        password = cls.validate_password(input("enter your password"),input("enter repeat password"))
        h_password = hash_password(password)
        if not(cls.users_file.find_row_item('username', username)):
            user_dict = {"type": cls.__name__, "username": username, "password": h_password}
            cls.users_file.add_to_file(user_dict)
            logging.info("new User Added")
        else:
            print("username Exist")

    # @classmethod
    # def check_login(cls):
    #     username = input("enter username")
    #     password = input("enter password")
    #     info_user = cls.users_file.find_row_item("username", username)
    #     if info_user["password"] == password:
    #         print(info_user)
    #         return info_user

    @classmethod
    def login_user(cls):
        username = cls.validate_username(input("enter username"))
        password = hash_password(input("enter password"))
        info_user = cls.users_file.find_row_item("username", username)
        if info_user["password"] == password:
            logging.info(f"{username} logg in")
            return info_user

        # user_login = cls.check_login()
        # print(user_login["type"])
        # cls.print_menu_access()

    @classmethod
    def print_menu_access(cls):
        print(f"your role:{cls.__name__}")

    @staticmethod
    def validate_username(username):
        if len(username) != 11 or not(username.isnumeric()):
            logging.info("Your username should be 11 character and should be number")
            raise Exception("Your username should be 11 character and should be number")

        else:
            return username



    @staticmethod
    def chek_format_time(store_time):
        try:
            datetime.datetime.strptime(store_time, '%H:%M')
            return store_time
        except ValueError:
            logging.info(f"{store_time} wrong format")
            print(f"{store_time} does not match format %H:%M")

    @staticmethod
    def validate_password(password, repeat_password):
        if password != repeat_password:
            logging.info("password and repeat password dos not match")
            raise Exception("password and repeat password dos not match")
        else:
            return password







# user1 = User()
# user1.register_user()




