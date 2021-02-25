"""
=================================
Author: Flora Chen
Time: 2021/1/27 21:23
-_- -_- -_- -_- -_- -_- -_- -_-
=================================
"""
import pytest,json
from requests import request
from middleware.handler import MidHandler


class TestLogin:
    """
    登录
    使用第一版多值断言
    使用了中间件
    使用正则表达式替换用例数据
    """
    test_data = MidHandler.excel.read("login")

    @pytest.mark.parametrize("data", test_data)
    def test_login(self, data):
        url = MidHandler.conf_data["ENV"]["BASE_URL"] + data["url"]
        method = data["method"]
        headers = MidHandler.conf_data["ENV"]["HEADER"]
        request_data = data["data"]
        expected = json.loads(data["expected"])

        if "#new_phone#" in request_data:
            request_data = request_data.replace("#new_phone#", MidHandler.generate_new_phone())

        if "#admin_phone#" in request_data:
            request_data = request_data.replace("#admin_phone#", MidHandler.security_data["admin_phone"])

        if "#admin_pwd#" in request_data:
            request_data = request_data.replace("#admin_pwd#", MidHandler.security_data["admin_pwd"])

        if "#investor_phone#" in request_data:
            request_data = request_data.replace("#investor_phone#", MidHandler.security_data["investor_phone"])

        if "#investor_pwd#" in request_data:
            request_data = request_data.replace("#investor_pwd#", MidHandler.security_data["investor_pwd"])

        response = request(url=url, method=method, headers=headers, json=json.loads(request_data))
        actual = response.json()

        try:
            for key, value in expected.items():
                print(key, value)
                assert actual[key] == value
        except AssertionError as e:
            test_result = "Failed"
            MidHandler.log.error(e)
            MidHandler.log.info(
                "\ncaseid: {}, title: {}\nurl: {}\nmethod: {}\nheader: {}\ncase_data: {}\nresponse: {}\nresult: {}\n".format(
                    data["case_id"], data["title"], url, method, headers, request_data,
                    response, test_result))
            raise e
        else:
            test_result = "Passed"
            MidHandler.log.info(
                "\ncaseid: {}, title: {}\nurl: {}\nmethod: {}\nheader: {}\ncase_data: {}\nresponse: {}\nresult: {}\n".format(
                    data["case_id"], data["title"], url, method, headers, request_data,
                    response, test_result))


if __name__ == "__main__":
    pytest.main(["test_login.py"])
