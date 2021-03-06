"""
=================================
Author: Flora Chen
Time: 2021/2/3 20:42
-_- -_- -_- -_- -_- -_- -_- -_-
=================================
"""
import pytest, json
from middleware.handler import MidHandler
from requests import request
from jsonpath import jsonpath


class TestAudit:
    """
    审核项目接口测试用例
    借款人登录新建项目
    管理员登录审核项目
    """
    test_data = MidHandler.excel.read("audit")

    @pytest.mark.parametrize("data", test_data)
    def test_audit(self, data, admin_login, add_loan, loan_login, db):
        # 动态设置类属性中需要的数据
        setattr(MidHandler, "admin_token", admin_login["authorization"])
        setattr(MidHandler, "loan_token", loan_login["authorization"])
        setattr(MidHandler, "loan_id", str(add_loan["id"]))

        # 使用正则表达式替换数据
        data = MidHandler.replace_data(json.dumps(data))
        data = json.loads(data)

        url = MidHandler.conf_data["ENV"]["BASE_URL"] + data["url"]
        method = data["method"]
        header = json.loads(data["header"])

        case = data["data"]
        expected = json.loads(data["expected"])

        # 修改项目的状态，不符合要求的项目状态，无法审核成功
        if '项目状态为2' in data['title']:
            sql = 'update loan set status=2 where id={}'.format(getattr(MidHandler, "loan_id"))
            db.update(sql)
        elif '项目状态为5' in data['title']:
            sql = 'update loan set status=5 where id={}'.format(getattr(MidHandler, "loan_id"))
            db.update(sql)
        elif '项目状态为3' in data['title']:
            sql = 'update loan set status=3 where id={}'.format(getattr(MidHandler, "loan_id"))
            db.update(sql)
        elif '项目状态为4' in data['title']:
            sql = 'update loan set status=4 where id={}'.format(getattr(MidHandler, "loan_id"))
            db.update(sql)

        response = request(url=url, method=method, json=json.loads(case), headers=header)
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
    pytest.main(["test_audit.py"])
