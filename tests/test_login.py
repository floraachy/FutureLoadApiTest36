"""
=================================
Author: Flora Chen
Time: 2021/1/27 21:23
-_- -_- -_- -_- -_- -_- -_- -_-
=================================
"""
import pytest
from requests import request
from middleware.handler import MidHandler


class TestLogin:
    """
    登录的测试用例
    """
    test_data = MidHandler.excel.read("login")

    @pytest.mark.parametrize("data", test_data)
    def test_login(self, data):
        url = MidHandler.conf_data["ENV"]["BASE_URL"] + data["url"]
        method = data["method"]
        headers = MidHandler.conf_data["ENV"]["HEADER"]
        request_data = data["data"]
        expected = eval(data["expected"])

        if "#new_phone#" in request_data:
            request_data = request_data.replace("#new_phone#", MidHandler.help.generate_new_phone())


        if "#admin_phone#" in request_data:
            request_data = request_data.replace("#admin_phone#", MidHandler.security_data["admin"])

        if "#admin_pwd#" in request_data:
            request_data = request_data.replace("#admin_pwd#", MidHandler.security_data["admin_pwd"])

        if "#user_phone#" in request_data:
            request_data = request_data.replace("#user_phone#", MidHandler.security_data["user"])

        if "#user_pwd#" in request_data:
            request_data = request_data.replace("#user_pwd#", MidHandler.security_data["user_pwd"])


        response = request(url=url, method=method, headers=headers, json=eval(request_data)).json()



        try:
            assert expected["code"] == response["code"]
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
