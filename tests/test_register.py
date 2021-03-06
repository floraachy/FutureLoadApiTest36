"""
=================================
Author: Flora Chen
Time: 2021/1/18 22:21
-_- -_- -_- -_- -_- -_- -_- -_-
=================================
"""
from requests import request
import pytest, json
from middleware.handler import MidHandler


class TestRegister:
    """
    注册
    使用第1版多值断言方式
    没有使用正则表达式替换数据，用的if判断替换用例数据，这里特意保留这种方式，作为对比
    使用了中间件
    """
    # 获取excel中的测试数据
    test_data = MidHandler.excel.read("register")

    @pytest.mark.parametrize("data", test_data)
    def test_register(self, data):
        # 获取测试数据
        request_url = MidHandler.conf_data["ENV"]["BASE_URL"] + data["url"]
        request_method = data["method"]
        case = data["data"]
        request_headers = json.loads(data["header"])
        expected = json.loads(data["expected"])

        # 生成一个未注册过的手机号码
        phone = MidHandler.generate_new_phone()

        if "#new_phone#" in case:
            case = case.replace("#new_phone#", phone)

        if "#exist_phone#" in case:
            case = case.replace("#exist_phone#", MidHandler.security_data["admin_phone"])

        # 获取请求结果
        response = request(method=request_method, url=request_url, json=json.loads(case), headers=request_headers)

        actual_result = response.json()

        # 断言
        try:
            assert actual_result["code"] == expected["code"]
            assert actual_result["msg"] == expected["msg"]
        except AssertionError as e:
            test_result = "Failed"
            MidHandler.log.error(e)
            MidHandler.log.info(
                "\ncaseid: {}, title: {}\nurl: {}\nmethod: {}\nheader: {}\ncase_data: {}\nresponse: {}\nresult: {}\n".format(
                    data["case_id"], data["title"], request_url, request_method, request_headers, case,
                    actual_result, test_result))
            raise e
        else:
            test_result = "Passed"
            MidHandler.log.info(
                "\ncaseid: {}, title: {}\nurl: {}\nmethod: {}\nheader: {}\ncase_data: {}\nresponse: {}\nresult: {}\n".format(
                    data["case_id"], data["title"], request_url, request_method, request_headers, case,
                    actual_result, test_result))


if __name__ == "__main__":
    pytest.main(["test_register.py"])
