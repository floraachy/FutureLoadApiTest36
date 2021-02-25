"""
======================================
Author: Flora.Chen
Time: 2021/2/24 22:23
~ _ ~ ~ _ ~ ~ _ ~ ~ _ ~ ~ _ ~ ~ _ ~
======================================
"""
import pytest, json
from middleware.handler import MidHandler
from requests import request


class TestUpdate:
    """
    更新会员信息
    """
    test_data = MidHandler.excel.read("update")

    @pytest.mark.parametrize("data", test_data)
    def test_update(self, data, admin_login, investor_login):
        url = MidHandler.conf_data["ENV"]["BASE_URL"] + data["url"]
        method = data["method"]
        header = json.loads(data["header"])

        case = data["data"]
        expected = json.loads(data["expected"])

        if "管理员修改昵称" in data["title"]:
            header["Authorization"] = admin_login["authorization"]
        else:
            header["Authorization"] = investor_login["authorization"]

        if "#investor_member_id#" in case:
            case = case.replace("#investor_member_id#", str(investor_login["id"]))

        if "#admin_member_id#" in case:
            case = case.replace("#admin_member_id#", str(admin_login["id"]))

        response = request(method=method, url=url, headers=header, json=json.loads(case))

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
    pytest.main(["test_update.py"])
