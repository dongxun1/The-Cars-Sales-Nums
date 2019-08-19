import pymysql
from Test.Homework.configs import *


class MYSQL(object):
    def __init__(self, host=MYSQL_HOST, username=MYSQL_USERNAME, password=MYSQL_PASSWORD, port=MYSQL_PORT,
                 database=MYSQL_DATABASE):
        """
        初始化Mysql
        :param host:
        :param username:
        :param password:
        :param port:
        :param database:
        """
        try:
            self.db = pymysql.connect(host, username, password, database, charset='utf8', port=port)
            self.cursor = self.db.cursor()
        except pymysql.MySQLError as e:
            print(e.args)

    def insert(self, data):
        """
        插入数据
        :param table:
        :param data:
        """
        keys = ', '.join(data.keys())
        values = ', '.join(['%s'] * len(data))
        table = 'aiocardata'
        sql_query = 'insert into %s (%s) values (%s)' % (table, keys, values)
        try:
            self.cursor.execute(sql_query, tuple(data.values()))
            self.db.commit()
        except pymysql.MySQLError as e:
            print(e.args)
            self.db.rollback()


