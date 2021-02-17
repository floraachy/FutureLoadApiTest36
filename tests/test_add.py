"""
=================================
Author: Flora Chen
Time: 2021/2/2 21:56
-_- -_- -_- -_- -_- -_- -_- -_-
=================================
"""

from requests import request
import pytest, json
from jsonpath import jsonpath
from middleware.handler import MidHandler


@pytest.mark.test
class TestAdd:
    """
    新增项目的测试用例
    """
    test_data = MidHandler.excel.read("add")

    @pytest.mark.parametrize("data", test_data)
    def test_add(self, data, investor_login, db):
        request_url = MidHandler.conf_data["ENV"]["BASE_URL"] + data["url"]
        request_method = data["method"]
        request_header = MidHandler.conf_data["ENV"]["HEADER"]
        authorization = investor_login["authorization"]
        request_header["Authorization"] = authorization
        request_data = data["data"]

        member_id =  investor_login["id"]

        if "#user_member_id#" in request_data:
            request_data = request_data.replace("#user_member_id#", str(member_id))

        response = request(url=request_url, method=request_method, headers=request_header,
                           json=json.loads(request_data))
        response_data = response.json()


        expected = json.loads(data["expected"])

        try:
            assert expected["code"] == response_data["code"]
        except AssertionError as e:
            MidHandler.log.error(e)
            MidHandler.log.info(
                "\ncaseid: {}, title: {}\nurl: {}\nmethod: {}\nheader: {}\ncase_data: {}\nresponse: {}\nresult: {}\n".format(
                    data["case_id"], data["title"], request_url, request_method, request_header, request_data,
                    response_data, "Failed"))
            raise e
        else:
            MidHandler.log.info(
                "\ncaseid: {}, title: {}\nurl: {}\nmethod: {}\nheader: {}\ncase_data: {}\nresponse: {}\nresult: {}\n".format(
                    data["case_id"], data["title"], request_url, request_method, request_header, request_data,
                    response_data, "Passed"))


if __name__ == "__main__":
    pytest.main(["test_add.py"])
