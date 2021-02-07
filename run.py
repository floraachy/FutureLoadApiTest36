"""
=================================
Author: Flora Chen
Time: 2021/1/18 22:17
-_- -_- -_- -_- -_- -_- -_- -_-
=================================
"""
# 主程序文件
import os, pytest
from datetime import datetime
from conf import path


current_time = datetime.now().strftime("%Y-%m-%d %H_%M_%S")

report_file = os.path.join(path.REPORT_DIR, "test_report_{}.html".format(current_time))

pytest.main(["--html={}".format(report_file)])
