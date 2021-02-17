"""
=================================
Author: Flora Chen
Time: 2021/1/30 13:16
-_- -_- -_- -_- -_- -_- -_- -_-
=================================
"""
import pytest
from requests import request
from jsonpath import jsonpath
from middleware.handler import MidHandler


def login(user, pwd):
    """
    登录的通用函数
    :param user: 用户名
    :param pwd: 密码
    :return:
    """
    url = MidHandler.conf_data["ENV"]["BASE_URL"] + MidHandler.conf_data["LOGIN"]["URL"]
    method = MidHandler.conf_data["LOGIN"]["METHOD"]
    headers = MidHandler.conf_data["ENV"]["HEADER"]
    data = {
        "mobile_phone": user,
        "pwd": pwd
    }

    response = request(method=method, url=url, headers=headers, json=data).json()

    return {
        "id": response["data"]["id"],
        "authorization": response["data"]["token_info"]["token_type"] + " " + response["data"]["token_info"]["token"],
        "leave_amount": response["data"]["leave_amount"]
    }


@pytest.fixture()
def admin_login():
    """
    登录接口： 管理员登录
    :return: response 响应数据
    """
    user = {
        "mobile_phone": MidHandler.security_data["admin"],
        "pwd": MidHandler.security_data["admin_pwd"]
    }

    return login(user["mobile_phone"], user["pwd"])


@pytest.fixture()
def investor_login():
    """
    登录接口: 普通用户登录，投资人
    :return: response 响应数据
    """
    user = {
        "mobile_phone": MidHandler.security_data["investor"],
        "pwd": MidHandler.security_data["investor_pwd"]
    }

    return login(user["mobile_phone"], user["pwd"])


@pytest.fixture()
def loan_login():
    """
    登录接口: 普通用户登录，借款人
    :return: response 响应数据
    """
    user = {
        "mobile_phone": MidHandler.security_data["loan"],
        "pwd": MidHandler.security_data["loan_pwd"]
    }

    return login(user["mobile_phone"], user["pwd"])

@pytest.fixture()
def add_loan(loan_login):
    url = MidHandler.conf_data["ENV"]["BASE_URL"] + MidHandler.conf_data["LOAN"]["URL"]
    method = MidHandler.conf_data["LOAN"]["METHOD"]
    headers = MidHandler.conf_data["ENV"]["HEADER"]
    headers["Authorization"] = loan_login["authorization"]
    data = {
        "member_id": loan_login["id"],
        "title": "flora借款项目",
        "amount": 120000,
        "loan_rate": 18.0,
        "loan_term": 6,
        "loan_date_type": 1,
        "bidding_days": 5
    }
    response = request(method=method, url=url, json=data, headers=headers).json()
    return {
        "id": response["data"]["id"]
    }


@pytest.fixture()
def recharge(amount, investor_login):
    """
    充值接口
    :return: response 响应数据
    """
    request_url = MidHandler.conf_data["ENV"]["BASE_URL"] + MidHandler.conf_data["RECHARGE"]["URL"]
    request_method = MidHandler.conf_data["RECHARGE"]["METHOD"]
    request_header = MidHandler.conf_data["ENV"]["HEADER"]
    authorization = loan_login["authorization"]
    request_header["Authorization"] = authorization
    request_data = {
        "member_id": loan_login["id"],
        "amount": amount
    }

    response = request(method=request_method, url=request_url, headers=request_header, json=request_data).json()

    return response


@pytest.fixture()
def db():
    """
    管理数据库连接的fixture
    好处是不用每次使用的时候都建立一次连接，并且关闭数据库。
    """
    db_conn = MidHandler.db_class()
    yield db_conn
    db_conn.close()


if __name__ == "__main__":
    # # print(login())
    # test = json.loads('{"member_id": "#user_member_id#", "amount": 500000}')
    # print(test, type(test))
    # if "#user_member_id#" in test:
    #     print("ok")
    print(recharge(500))

"""
{'code': 0, 'msg': 'OK', 
'data': {'id': 867, 'leave_amount': 2000001.11, 'mobile_phone': '13504936561', 'reg_name': '007', 'reg_time': '2021-01-28 21:59:59.0', 'type': 1, 
'token_info': 
{'token_type': 'Bearer', 'expires_in': '2021-01-30 22:29:26', 
'token': 'eyJhbGciOiJIUzUxMiJ9.eyJtZW1iZXJfaWQiOjg2NywiZXhwIjoxNjEyMDE2OTY2fQ.S4X19WLex29QBee9O3H4wZ8QGtBNvjTp8BtmPcq9pxSh4l8dxKFjQJuCr-HA4Q8ywmrKrbao2IW3k9I21QrT-w'}}, 'copyright': 'Copyright 柠檬班 © 2017-2020 湖南省零檬信息技术有限公司 All Rights Reserved'
}
"""
