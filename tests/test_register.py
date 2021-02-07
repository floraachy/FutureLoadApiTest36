"""
=================================
Author: Flora Chen
Time: 2021/1/18 22:21
-_- -_- -_- -_- -_- -_- -_- -_-
=================================
"""
from requests import request
import pytest
from middleware.handler import MidHandler


class TestRegister:
    """
    注册的测试用例, 使用了中间件
    """
    # 获取excel中的测试数据
    test_data = MidHandler.excel.read("register")

    @pytest.mark.parametrize("data", test_data)
    def test_register(self, data):
        """
        注册用例
        :param data: 测试数据
        :return:
        """
        # 获取测试数据
        request_url = MidHandler.conf_data["ENV"]["BASE_URL"] + data["url"]
        request_method = data["method"]
        request_json = data["data"]

        request_headers = MidHandler.conf_data["ENV"]["HEADER"]
        expected = eval(data["expected"])

        # 生成一个未注册过的手机号码
        phone = MidHandler.generate_new_phone()


        if "#new_phone#" in request_json:
            request_json = request_json.replace("#new_phone#", phone)

        if "#exist_phone#" in request_json:
            actual_json = request_json.replace("#exist_phone#", MidHandler.security_data["user"])

        # 获取请求结果
        actual_result = request(method=request_method, url=request_url, json=eval(request_json), headers=request_headers).json()

        # 断言
        try:
            # 第一版多值断言
            # assert actual_result["code"] == expected["code"]
            # assert actual_result["msg"] == expected["msg"]

            # 第二版多值断言
            for key, value in expected.items():
                assert actual_result["key"] == value

            # 第三版断言
            """
            jsonpath的表达式作为key放置在预期结果的字典里面
            expected = {"$..code": 0, "$..msg": "OK"}
            for key, value in expected.items():
                # 实际结果：jsonpath(actual_result, key) 
                assert jsonpath(actual_result, key)[0] == value
            """
        except AssertionError as e:
            test_result = "Failed"
            MidHandler.log.error(e)
            MidHandler.log.info("\ncaseid: {}, title: {}\nurl: {}\nmethod: {}\nheader: {}\ncase_data: {}\nresponse: {}\nresult: {}\n".format(data["case_id"], data["title"], request_url, request_method, request_headers, request_json, actual_result, test_result))
            raise e
        else:
            test_result = "Passed"
            MidHandler.log.info("\ncaseid: {}, title: {}\nurl: {}\nmethod: {}\nheader: {}\ncase_data: {}\nresponse: {}\nresult: {}\n".format(data["case_id"], data["title"], request_url, request_method, request_headers, request_json, actual_result, test_result))


if __name__ == "__main__":
    pytest.main(["test_register.py"])
