import hashlib


def hash_password(password):
    h_pass = hashlib.sha256(password.encode()).hexdigest()
    return h_pass
#برای تبدیل stبه لیست

def list_parser(st):
    l_x = [i for i in eval(st)]
    return l_x


