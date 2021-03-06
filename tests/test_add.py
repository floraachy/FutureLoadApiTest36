"""
=================================
Author: Flora Chen
Time: 2021/2/2 21:56
-_- -_- -_- -_- -_- -_- -_- -_-
=================================
"""

from requests import request
import pytest, json
from middleware.handler import MidHandler
from jsonpath import jsonpath



class TestAdd:
    """
    新增项目的测试用例
    """
    test_data = MidHandler.excel.read("add")

    @pytest.mark.parametrize("data", test_data)
    def test_add(self, data, investor_login, db):
        # 动态设置类属性中需要的数据
        setattr(MidHandler, "investor_member_id", str(investor_login["id"]))
        setattr(MidHandler, "investor_token", investor_login["authorization"])

        # 使用正则表达式替换数据
        data = MidHandler.replace_data(json.dumps(data))
        data = json.loads(data)

        request_url = MidHandler.conf_data["ENV"]["BASE_URL"] + data["url"]
        request_method = data["method"]
        request_data = data["data"]
        request_header = json.loads(data["header"])

        response = request(url=request_url, method=request_method, headers=request_header,
                           json=json.loads(request_data))
        response_data = response.json()

        expected = json.loads(data["expected"])

        try:
            for key, value in expected.items():
                assert jsonpath(response_data, key)[0] == value
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
