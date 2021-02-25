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

class TestInfo:
    """
    获取单个会员信息
    """
    test_data = MidHandler.excel.read("info")

    @pytest.mark.parametrize("data", test_data)
    def test_info(self, data, admin_login, investor_login):
        url =MidHandler.conf_data["ENV"]["BASE_URL"] + data["url"]
        method = data["method"]
        header = json.loads(data["header"])
        expected = json.loads(data["expected"])

        if "#admin_member_id#" in data["url"]:
            url = url.replace("#admin_member_id#", str(admin_login["id"]))

        if "#investor_member_id#" in data["url"]:
            url = url.replace("#investor_member_id#", str(investor_login["id"]))

        if "管理员" in data["title"]:
            header["Authorization"] = admin_login["authorization"]
        else:
            header["Authorization"] = investor_login["authorization"]

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
    pytest.main(["test_info.py"])
