"""
=================================
Author: Flora Chen
Time: 2021/1/20 20:34
-_- -_- -_- -_- -_- -_- -_- -_-
=================================
"""

import yaml


def read_yaml(file):
    """
    读取yaml文件
    :param file: 文件路径
    :return:
    """
    with open(file, "r", encoding="utf-8") as f:
        # return yaml.load(f, Loader=yaml.FullLoader)
        return yaml.load(f, Loader=yaml.SafeLoader)  #解析更安全

# # 获取配置文件中的数据
# conf_data = read_yaml(os.path.join(CONF_DIR, "conf.yaml"))
#
# # 获取账户信息
# user_data = read_yaml(os.path.join(CONF_DIR, "security.yaml"))