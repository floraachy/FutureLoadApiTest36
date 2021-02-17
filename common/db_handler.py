"""
=================================
Author: Flora Chen
Time: 2021/1/20 20:33
-_- -_- -_- -_- -_- -_- -_- -_-
=================================
"""
import pymysql


class DBHandler:
    """
    数据库操作
    """

    def __init__(self,
                 host=None,
                 port=None,
                 user=None,
                 password=None,
                 database=None,
                 charset="utf8",
                 cursorclass=pymysql.cursors.DictCursor  # 加上这个返回的就是字典
                 ):
        """
        初始化方法中， 连接到数据库
        """

        # 建立连接
        self.conn = pymysql.connect(host=host,
                                    port=port,
                                    user=user,
                                    password=password,
                                    database=database,
                                    charset=charset,
                                    cursorclass=cursorclass
                                    )

    def query_all(self, sql):
        """
        查询所有符合sql条件的数据
        :param sql: 执行的sql
        :return: 查询结果
        """
        # 创建一个游标对象
        self.cursor = self.conn.cursor()
        self.conn.commit()
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        self.cursor.close()
        return data

    def query_one(self, sql):
        """
        查询符合sql条件的数据的第一条数据
        :param sql: 执行的sql
        :return: 返回查询结果的第一条数据
        """
        # 创建一个游标对象
        self.cursor = self.conn.cursor()

        self.conn.commit()
        self.cursor.execute(sql)
        data = self.cursor.fetchone()
        self.cursor.close()
        return data

    def insert(self, sql):
        """
        插入数据
        :param sql: 执行的sql
        """
        # 创建一个游标对象
        self.cursor = self.conn.cursor()

        self.cursor.execute(sql)
        # 提交  只要数据库更新就要commit
        self.conn.commit()

        self.cursor.close()

    def update(self, sql):
        """
        更新数据
        :param sql: 执行的sql
        """
        # 创建一个游标对象
        self.cursor = self.conn.cursor()

        self.cursor.execute(sql)
        # 提交 只要数据库更新就要commit
        self.conn.commit()

        self.cursor.close()

    def query(self, sql, one=True):
        """
        根据传值决定查询一条数据还是所有
        :param one: 默认True. True查一条数据，否则查所有
        :return:
        """
        if one:
            return self.query_one(sql)
        else:
            return self.query_all(sql)

    def close(self):
        """
        断开游标，关闭数据库
        :return:
        """
        self.conn.close()


if __name__ == "__main__":
    db = DBHandler()
    # data = db.query_all("SELECT mobile_phone from member limit 1;")
    # print(data[0]["mobile_phone"])
    # print(type(data))
    member_id = db.query_one("select id from member where mobile_phone=13504936561;")["id"]
    print(member_id, type(member_id))
    leave_amount = db.query_one("select leave_amount from member where mobile_phone=13504936561;")["leave_amount"]
    print(leave_amount)
    add_mount = db.update("update member set leave_amount={} where id={};".format(500, member_id))

    leave_amount_after = db.query_one("select leave_amount from member where mobile_phone=13504936561;")["leave_amount"]
    print(leave_amount_after)
    db.close()

"""
1. 建立连接
2. 获取游标
3. 通过游标执行sql语句
4. 通过游标得到结果
"""
"""
# 建立连接
conn = pymysql.connect(host="8.129.91.152",
                       port=3306,
                       user="future",
                       password="123456",
                       # 注意： 不要写成utf-8
                       charset="utf8",
                       database="futureloan" # 这里指定数据库名称后，后面SQL语句就不需要带数据库名称了
                       )
# 获取游标
cursor = conn.cursor()

# 通过游标执行sql语句
# cursor.execute("SELECT * FROM futureloan.member LIMIT 10;")
cursor.execute("SELECT * FROM member LIMIT 10;")
cursor.execute("SELECT * FROM member WHERE id={};".format(1))

# 通过游标得到结果 - 查询所有
# data = cursor.fetchall()

# 通过游标得到结果 - 查询一条数据
data = cursor.fetchone()
print(data)

# 断开游标，关闭数据库
cursor.close()
conn.close()

"""
