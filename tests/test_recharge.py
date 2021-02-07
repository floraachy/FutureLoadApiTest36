"""
=================================
Author: Flora Chen
Time: 2021/1/29 20:15
-_- -_- -_- -_- -_- -_- -_- -_-
=================================
"""
"""
充值
-member_id  需要登录接口返回


登录接口作用：
-得到id
-得到token
-得到leave_amount


充值接口依赖于登录解耦
登录是充值接口的前置条件
使用pytest当中的fixture实现前置条件
"""
from requests import request
from middleware.handler import MidHandler
import pytest, json
from jsonpath import jsonpath

# @pytest.mark.test
class TestRecharge:
    """
    充值接口测试， 调接口检查是否充值成功
    """
    test_data = MidHandler.excel.read("recharge")

    @pytest.mark.parametrize("data", test_data)
    def test_recharge(self, data, investor_login, db):
        request_url = MidHandler.conf_data["ENV"]["BASE_URL"] + data["url"]
        request_method = data["method"]
        request_header = MidHandler.conf_data["ENV"]["HEADER"]
        authorization = investor_login["authorization"]
        request_header["Authorization"] = authorization
        request_data = data["data"]

        leave_amount_before = investor_login["leave_amount"]

        if "#user_member_id#" in request_data:
            member_id = db.query_one("select id from member where mobile_phone={};".format(MidHandler.security_data["user"]))["id"]
            request_data = request_data.replace("#user_member_id#", str(member_id))

        if "#wrong_member_id#" in request_data:
            request_data = request_data.replace("#wrong_member_id#", "0012")

        response = request(url=request_url, method=request_method, headers=request_header, json=json.loads(request_data)).json()



        expected = eval(data["expected"])

        if response["code"] == 0:
            leave_amount_after = jsonpath(response, "$.data.leave_amount")[0]


        try:
            assert expected["code"] == response["code"]
            if "充值成功" in data["title"]:
                assert leave_amount_after - leave_amount_before == json.loads(request_data)["amount"]
        except AssertionError as e:
            MidHandler.log.error(e)
            MidHandler.log.info(
                "\ncaseid: {}, title: {}\nurl: {}\nmethod: {}\nheader: {}\ncase_data: {}\nresponse: {}\nresult: {}\n".format(
                    data["case_id"], data["title"], request_url, request_method, request_header, request_data,
                    response, "Failed"))
            raise e
        else:
            MidHandler.log.info(
                "\ncaseid: {}, title: {}\nurl: {}\nmethod: {}\nheader: {}\ncase_data: {}\nresponse: {}\nresult: {}\n".format(
                    data["case_id"], data["title"], request_url, request_method, request_header, request_data,
                    response, "Passed"))


if __name__ == "__main__":
    pytest.main(["-m test"])


"""jsonpath: 帮助我们快速找到json数据的某个字段
"""

"""
json序列化和反序列化
json.loads()：把json格式的字符串转成python当中的字典  -- > 反序列化
json.dumps(): python中的字典转成json格式的字符串    -- > 序列化

import json

# 反序列化
a_str = '{"username": "yz", "age": 10}'
res = json.loads(a_str)
print(res, type(res))  # 输出：{'username': 'yz', 'age': 10} <class 'dict'>

# 序列化
b_dict = {"username": "中文", "age": 10}
res1 = json.dumps(b_dict)
print(res1, type(res1)) # 输出：{"username": "\u4e2d\u6587", "age": 10} <class 'str'>
"""