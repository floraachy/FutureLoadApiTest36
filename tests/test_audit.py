"""
=================================
Author: Flora Chen
Time: 2021/2/3 20:42
-_- -_- -_- -_- -_- -_- -_- -_-
=================================
"""
import pytest

class TestAudit:
    """
    审核项目接口测试用例
    借款人登录新建项目
    管理员登录审核项目
    """
    def test_audit(self, admin_login):
        print(admin_login)



if __name__ == "__main__":
    pytest.main(["test_audit.py"])
