"""
======================================
Author: Flora.Chen
Time: 2021/2/24 22:23
~ _ ~ ~ _ ~ ~ _ ~ ~ _ ~ ~ _ ~ ~ _ ~ 
======================================
"""
import pytest,json
from middleware.handler import MidHandler
from requests import request

class TestLoans:
    """
    分页获取项目列表
    """
    test_data = MidHandler.excel.read("loans")

    @pytest.mark.parametrize("data", test_data)
    def test_loans(self, data, admin_login):
        url =MidHandler.conf_data["ENV"]["BASE_URL"] + data["url"]
        method = data["method"]
        header = json.loads(data["header"])
        expected = json.loads(data["expected"])

        response = request(method=method, url=url, headers=header)

        response_data = response.json()

        try:
            assert expected["code"] == response_data["code"]
        except AssertionError as e:
            MidHandler.log.error(e)
            MidHandler.log.info(
                "\ncaseid: {}, title: {}\nurl: {}\nmethod: {}\nheader: {}\ncase_data: {}\nresponse: {}\nresult: {}\n".format(
                    data["case_id"], data["title"], url, method, header, data,
                    response_data, "Failed"))
            raise e
        else:
            MidHandler.log.info(
                "\ncaseid: {}, title: {}\nurl: {}\nmethod: {}\nheader: {}\ncase_data: {}\nresponse: {}\nresult: {}\n".format(
                    data["case_id"], data["title"], url, method, header, data,
                    response_data, "Passed"))


if __name__ == "__main__":
    pytest.main(["test_loans.py"])
