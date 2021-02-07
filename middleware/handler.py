"""
=================================
Author: Flora Chen
Time: 2021/2/1 21:17
-_- -_- -_- -_- -_- -_- -_- -_-
=================================
"""
import os
from conf.path import LOG_DIR, CONF_DIR, DATA_DIR
from common.logger_handler import get_logger
from common.yaml_handler import read_yaml
from common.excel_handler import ExcelHandler
from common import helper
from common.db_handler import DBHandler
import pymysql


class MidDBHandler(DBHandler):
    """
    def __init__(self,
                 host = Handler.security_data["MYSQL"]["HOST"],
                port = Handler.security_data["MYSQL"]["PORT"],
                user = Handler.security_data["MYSQL"]["USER"],
                password = Handler.security_data["MYSQL"]["PWD"],
                database = Handler.security_data["MYSQL"]["NAME"],
                charset="utf8",
                cursorclass=pymysql.cursors.DictCursor):
        super.__init__(host=host,
                       port=port,
                       user=user,
                       password=password,
                       database=database,
                       charset=charset,
                       cursorclass=cursorclass)
    # 下面的写法跟上面是一样的。
    """
    # 下面这种方法， 每次调用的时候不需要传参数了
    def __init__(self):
        # 获取账户信息
        security_data = read_yaml(os.path.join(CONF_DIR, "security.yaml"))

        super().__init__(
            host=security_data["MYSQL"]["HOST"],
            port=security_data["MYSQL"]["PORT"],
            user=security_data["MYSQL"]["USER"],
            password=security_data["MYSQL"]["PWD"],
            database=security_data["MYSQL"]["NAME"],
            charset="utf8",
            cursorclass=pymysql.cursors.DictCursor
            )


class MidHandler:
    """
    中间层。common和调用的中间层。
    使用项目的配置数据， 填充common模块。
    作用：
        1. 隔离代码，让common更通用
        2. 使用common代码更加简单，少调用
    """
    # 获取配置文件中的数据
    conf_data = read_yaml(os.path.join(CONF_DIR, "conf.yaml"))

    # 获取账户信息
    security_data = read_yaml(os.path.join(CONF_DIR, "security.yaml"))

    # 初始化log
    log = get_logger(file=os.path.join(LOG_DIR,conf_data["LOG"]["FILENAME"]),
                     name=conf_data["LOG"]["NAME"],
                     level=conf_data["LOG"]["LEVEL"],
                     handler_level=conf_data["LOG"]["HANDLER_LEVEL"],
                     file_level=conf_data["LOG"]["FILE_LEVEL"],
                     fmt=conf_data["LOG"]["FMT"])

    # excel对象
    # 获取excel的路径
    excel_file = os.path.join(DATA_DIR, "case.xlsx")
    excel = ExcelHandler(excel_file)


    """
    # 数据库
    db = DBHandler(host = security_data["MYSQL"]["HOST"],
    port = security_data["MYSQL"]["PORT"],
    user = security_data["MYSQL"]["USER"],
    password = security_data["MYSQL"]["PWD"],
    database = security_data["MYSQL"]["NAME"]
    )
    """
    # 数据库  下面这种写法是重命名
    db_class = MidDBHandler

    # 新手机号码
    new_phone = ""

    # 投资人信息
    investor_user_id = ""
    investor_user_token = ""

    # 借款人信息
    loan_user_id = ""
    loan_user_token = ""

    # 管理员信息
    admin_user_id = ""
    admin_user_token = ""


    @classmethod
    def generate_new_phone(cls):
        """
        获取一个数据库中未注册过的手机号码
        :return: 未注册的手机号码
        """
        while True:
            phone = helper.generate_phone()
            db = MidDBHandler()
            result = db.query_all("SELECT mobile_phone from member where mobile_phone={};".format(phone))
            db.close()
            if not result:
                cls.new_phone = phone
                return phone


if __name__ == "__main__":
    pass




