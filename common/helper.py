"""
=================================
Author: Flora Chen
Time: 2021/1/25 21:23
-_- -_- -_- -_- -_- -_- -_- -_-
=================================
"""

"""
帮助模块
"""
from faker import Faker
import random

def generate_phone():
    """
    自动生成手机号码
    :return: 生成的手机号码
    """
    fk = Faker(locale="zh_CN")
    # fk.address() # 地址
    # fk.name() # 姓名
    return fk.phone_number()

# def generate_new_phone():
#     """
#     自动生成未注册过的手机号码
#     :return: 生成的手机号码
#     """
#     fk = Faker(locale="zh_CN")
#     while True:
#         phone = fk.phone_number()
#         db = DBHandler()
#         result = db.query_all("SELECT mobile_phone from member where mobile_phone={};".format(phone))
#         db.close()
#         if not result:
#             return phone

def generate_phone_copy():
    """
    自动生成手机号码
    :return: 生成的手机号码
    """
    while True:
        phone = "1" + random.choice(["3", "5", "7", "8", "9"])
        for i in range(9):
            number = random.randint(0, 9)
            phone += str(number) # phone = str(phone) + str(number)

        return phone



if __name__ == "__main__":
    print(generate_phone())
    print(generate_phone_copy())

