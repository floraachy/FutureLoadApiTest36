"""
=================================
Author: Flora Chen
Time: 2021/1/18 22:21
-_- -_- -_- -_- -_- -_- -_- -_-
=================================
"""

import logging

def get_logger(name,
               level,
               fmt,
               handler_level,
               file_level,
               file=None):
    """
    日志收集器
    :param name: 日志收集器名称
    :param level: 日志收集等级
    :param fmt: 日志输出格式
    :param handler_level: 控制台输出日志最低等级
    :param file_level: 文件输出日志最低等级
    :param file: 日志文件路径
    :return: logger 日志收集器
    """
    # 创建日志收集器
    logger = logging.getLogger(name)

    # 设置日志收集器收集等级
    logger.setLevel(level)

    # 创建日志输出渠道-控制台
    handler = logging.StreamHandler()

    # 设置日志收集等级-控制台
    handler.setLevel(handler_level)

    # 创建一个日志输出格式对象
    fmt = logging.Formatter(fmt)

    # 设置日志输出格式 - 控制台
    handler.setFormatter(fmt)

    # 添加日志处理器-控制台
    logger.addHandler(handler)

    if file:
        # 创建日志输出渠道-文件
        file_handler = logging.FileHandler(file, encoding="utf-8")

        # 设置日志收集等级-文件
        file_handler.setLevel(file_level)

        # 设置日志输出格式 - 文件
        file_handler.setFormatter(fmt)

        # 添加日志处理器-文件
        logger.addHandler(file_handler)

    return logger


# log = get_logger(file=os.path.join(LOG_DIR, "test.log"))

