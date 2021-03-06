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
from jsonpath import jsonpath


class TestUpdate:
    """
    更新会员信息
    """
    test_data = MidHandler.excel.read("update")

    @pytest.mark.parametrize("data", test_data)
    def test_update(self, data, admin_login, investor_login):
        # 动态设置类属性中需要的用户id
        setattr(MidHandler, "admin_member_id", str(admin_login["id"]))
        setattr(MidHandler, "investor_member_id", str(investor_login["id"]))
        setattr(MidHandler, "admin_token", admin_login["authorization"])
        setattr(MidHandler, "investor_token", investor_login["authorization"])

        # 使用正则表达式替换数据
        data = MidHandler.replace_data(json.dumps(data))
        data = json.loads(data)

        url = MidHandler.conf_data["ENV"]["BASE_URL"] + data["url"]
        method = data["method"]
        header = json.loads(data["header"])

        case = data["data"]
        expected = json.loads(data["expected"])

        response = request(method=method, url=url, headers=header, json=json.loads(case))

        response_data = response.json()

        try:
            for key, value in expected.items():
                assert jsonpath(response_data, key)[0] == value
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
