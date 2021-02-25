"""
=================================
Author: Flora Chen
Time: 2021/1/30 23:06
-_- -_- -_- -_- -_- -_- -_- -_-
=================================
"""
from requests import request
import pytest, json
from jsonpath import jsonpath
from decimal import Decimal
from middleware.handler import MidHandler

class TestWithdraw:
    """
    提现接口测试， 查数据库检查是否提现成功
    """
    test_data = MidHandler.excel.read("withdraw")

    @pytest.mark.parametrize("data", test_data)
    def test_withdraw(self, data, investor_login, db):
        request_url = MidHandler.conf_data["ENV"]["BASE_URL"] + data["url"]
        request_method = data["method"]
        request_header = MidHandler.conf_data["ENV"]["HEADER"]
        authorization = investor_login["authorization"]
        request_header["Authorization"] = authorization
        request_data = data["data"]

        member_id = investor_login["id"]

        if "#user_member_id#" in request_data:
            request_data = request_data.replace("#user_member_id#", str(member_id))

        if "#wrong_member_id#" in request_data:
            request_data = request_data.replace("#wrong_member_id#", "0012")

        if "小于用户可用余额， 提现成功" in data["title"]:
            amount = json.loads(request_data)["amount"] + 100
            db.update("update member set leave_amount={} where id={};".format(amount, member_id))

        if " 等于用户可用余额，提现成功" in data["title"]:
            db.update(
                "update member set leave_amount={} where id={};".format(json.loads(request_data)["amount"], member_id))

        leave_amount = db.query_one("select leave_amount from member where id={};".format(member_id))[
            "leave_amount"].quantize(Decimal('0.00'))

        response = request(url=request_url, method=request_method, headers=request_header,
                           json=json.loads(request_data))
        response_data = response.json()

        # leave_amount_after = db.query_one("select leave_amount from member where id={};".format(member_id))["leave_amount"]
        if "提现成功" in data["title"]:
            leave_amount_after = Decimal(jsonpath(response_data, "$.data.leave_amount")[0]).quantize(Decimal('0.00'))

        expected = json.loads(data["expected"])

        try:
            assert expected["code"] == response_data["code"]
            if "提现成功" in data["title"]:
                assert leave_amount - Decimal(json.loads(request_data)["amount"]).quantize(
                    Decimal('0.00')) == leave_amount_after
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
    pytest.main(["-m test"])
