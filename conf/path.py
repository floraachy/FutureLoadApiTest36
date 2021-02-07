"""
=================================
Author: Flora Chen
Time: 2021/1/20 20:24
-_- -_- -_- -_- -_- -_- -_- -_-
=================================
"""

import os


# 测试报告的路径
REPORT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "reports")
if not os.path.exists(REPORT_DIR):
    os.mkdir(REPORT_DIR)

# 测试日志的路径
LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs")
if not os.path.exists(LOG_DIR):
    os.mkdir(LOG_DIR)

# 测试数据的路径
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")

# 测试用例的路径
CASE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "tests")

# 配置文件的路径
CONF_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "conf")

# 公共模块的路径
COMMON_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "common")