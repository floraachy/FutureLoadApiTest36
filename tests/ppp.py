import logging, time
from logging.handlers import RotatingFileHandler

logger = logging.getLogger("py36")
# 初始化handler
handler = RotatingFileHandler("py.log",
                              maxBytes=100,
                              backupCount=3,
                              encoding="utf-8")

logger.addHandler(handler)

# 打印日志
for i in range(100):
    logger.warning("生成警告信息{}".format(time.time()))
    time.sleep(0.1)
