"""
======================================
Author: Flora.Chen
Time: 2021/2/17 21:13
~ _ ~ ~ _ ~ ~ _ ~ ~ _ ~ ~ _ ~ ~ _ ~ 
======================================
"""

from requests import request
import pytest, json
from jsonpath import jsonpath
from middleware.handler import MidHandler



class TestInvest:
    """
    投资项目的测试用例
    """
    test_data = MidHandler.excel.read("invest")

    @pytest.mark.parametrize("data", test_data)
    def test_invest(self, data, db):
        # 注意： 要保证替换成功必须保证excel中需要替换的字符串与保存数据类中的属性名一致
        data = MidHandler.replace_data(json.dumps(data))
        # 由于上面进行替换的时候，用例数据转换成字符串了，因此我们需要再转成字典格式
        data = json.loads(data)

        request_url = MidHandler.conf_data["ENV"]["BASE_URL"] + data["url"]
        request_method = data["method"]
        request_header = json.loads(data["header"])
        request_data = data["data"]

        if "用户余额大于投资金额" in data["title"]:
            amount = int(json.loads(request_data)["amount"]) + 1
            db.update("update member set leave_amount={}; ".format(amount))

        if "项目可投金额小于用户投资金额" in data["title"]:
            amount = int(json.loads(request_data)["amount"]) - 1
            db.update("update loan set amount={}; ".format(int(amount)))

        # 投资非竞标中的项目，修改项目的状态
        if '审核中1' in data['title']:
            sql = 'update loan set status=1 where id={}'.format(getattr(MidHandler, 'loan_id'))
            db.update(sql)
        elif '审核不通过5' in data['title']:
            sql = 'update loan set status=5 where id={}'.format(getattr(MidHandler, 'loan_id'))
            db.update(sql)
        elif '还款中3' in data['title']:
            sql = 'update loan set status=3 where id={}'.format(getattr(MidHandler, 'loan_id'))
            db.update(sql)
        elif '还款完成4' in data['title']:
            sql = 'update loan set status=4 where id={}'.format(getattr(MidHandler, 'loan_id'))
            db.update(sql)

        response = request(url=request_url, method=request_method, headers=request_header,
                           json=json.loads(request_data))
        response_data = response.json()

        if data["extractor"]:
            extractors = json.loads(data["extractor"])
            for name, expression in extractors.items():
                value = jsonpath(response_data, expression)[0]
                setattr(MidHandler, name, value)

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
    pytest.main(["test_invest.py"])
