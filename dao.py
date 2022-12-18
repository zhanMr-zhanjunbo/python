import random

import pymysql
import crawling as CRAW
from multiprocessing.dummy import Pool
from functools import partial

tables_list = ['contractLaw', 'laborLaw', 'trafficSafetyLaw', 'marriageLaw', 'successionLaw']
keywords_list = ["合同诈骗", "劳动仲裁", "交通安全事故", "离婚案件", "遗产继承"]


def create_database(ip='localhost', usr='root', pwd='microsys'):
    try:
        db = pymysql.connect(host=ip, user=usr, passwd=pwd, port=3306, charset='utf8')
        cursor = db.cursor()  # 创建游标对象
        cursor.execute("DROP DATABASE IF EXISTS lawInfo")
        cursor.execute("CREATE DATABASE IF NOT EXISTS lawInfo;")
        print("create database success!")
        cursor.execute("use lawInfo;")
        for table in tables_list:
            sql_table = f'''create table if not exists {table}(
                    id int not null primary key auto_increment,
                    title varchar(100) unique,
                    content varchar(500),
                    link varchar(255)
                    );'''
            cursor.execute(sql_table)
        sql_user = '''create table if not exists user(
                    id int not null primary key auto_increment,
                    account varchar(20),
                    password varchar(16),
                    passwd varchar(16),
                    telephone varchar(11) unique
                    );
        '''
        cursor.execute(sql_user)
        sql_consult = '''create table if not exists communication(
                    id int not null primary key auto_increment,
                    title varchar(30) unique,
                    content varchar(200),
                    is_public varchar(3),
                    user_id int,
                    crate_time timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    foreign key(user_id) references user(id) 
                    on update cascade #同步更新
                    on delete cascade #同步删除
                    );       
        '''
        cursor.execute(sql_consult)
        print("create table success!")
        cursor.close()
        db.close()  # 关闭数据库的连接
    except:
        print('something wrong!')


def search_title(ip='localhost', usr='root', pwd='microsys', id="1", title="title", start="2022-12-16 20",
                 end="2022-12-16 20"):
    try:
        db = pymysql.connect(host=ip, user=usr, passwd=pwd, port=3306, charset='utf8', database='lawInfo')
        cursor = db.cursor()  # 创建游标对象
        print("connect is success!")
        print(title, start, end, id)
        sql_db = f'''
                SELECT title,content FROM communication WHERE (crate_time>STR_TO_DATE('{start}','%Y-%m-%d %H') AND 
                crate_time<STR_TO_DATE('{end}','%Y-%m-%d %H') OR title='{title}') AND user_id='{id}';
        '''
        print(sql_db)
        cursor.execute(sql_db)
        results = cursor.fetchall()
        cursor.close()
        db.close()  # 关闭数据库的连接
        return results
    except:
        print("错误：没有查找到数据")


def search_one_title(ip='localhost', usr='root', pwd='microsys', id="1", title="title", start="2022-12-16 20",
                     end="2022-12-16 20"):
    try:
        db = pymysql.connect(host=ip, user=usr, passwd=pwd, port=3306, charset='utf8', database='lawInfo')
        cursor = db.cursor()  # 创建游标对象
        print("connect is success!")
        print(title, start, end, id)
        sql_db = f'''
                SELECT title,content FROM communication WHERE crate_time>STR_TO_DATE('{start}','%Y-%m-%d %H') AND 
                crate_time<STR_TO_DATE('{end}','%Y-%m-%d %H') AND title='{title}' AND user_id='{id}';
        '''
        print(sql_db)
        cursor.execute(sql_db)
        results = cursor.fetchall()
        cursor.close()
        db.close()  # 关闭数据库的连接
        return results
    except:
        print("错误：没有查找到数据")


def find_user_title(ip='localhost', usr='root', pwd='microsys', id="1"):
    try:
        db = pymysql.connect(host=ip, user=usr, passwd=pwd, port=3306, charset='utf8', database='lawInfo')
        cursor = db.cursor()  # 创建游标对象
        print("connect is success!")
        sql_db = '''
                SELECT title,content FROM communication WHERE user_id='%s';
        ''' % (id)
        print(sql_db)
        cursor.execute(sql_db)
        results = cursor.fetchall()
        cursor.close()
        db.close()  # 关闭数据库的连接
        return results
    except:
        print("错误：没有查找到数据")


def find_public_title(ip='localhost', usr='root', pwd='microsys'):
    try:
        db = pymysql.connect(host=ip, user=usr, passwd=pwd, port=3306, charset='utf8', database='lawInfo')
        cursor = db.cursor()  # 创建游标对象
        print("connect is success!")
        sql_db = '''
                SELECT title,content FROM communication WHERE is_public='yes';
        '''
        print(sql_db)
        cursor.execute(sql_db)
        results = cursor.fetchall()
        cursor.close()
        db.close()  # 关闭数据库的连接
        return results
    except:
        print("错误：没有查找到数据")


def insert_leave(ip='localhost', usr='root', pwd='microsys', title="民事诉讼与刑事诉讼的区别是什么？",
                 content="刑事诉讼和民事诉讼的区别为提起诉讼的主体不同；举证的责任不同；适用的法律不同；案件性质的不同；是否使用调解不同", is_public="yes",
                 account="anonymous"):
    try:
        db = pymysql.connect(host=ip, user=usr, passwd=pwd, port=3306, charset='utf8', database='lawInfo')
        cursor = db.cursor()  # 创建游标对象
        print("connect is success!")
        sql_id = "select id from user where account='%s';" % account
        cursor.execute(sql_id)
        id = cursor.fetchone()[0]
        sql_db = '''
                INSERT IGNORE INTO communication(title, content, is_public, user_id) VALUES('%s', '%s', '%s','%s') 
                ON DUPLICATE KEY UPDATE title=VALUES(title);
        ''' % (title, content, is_public, id)
        print(sql_db)
        cursor.execute(sql_db)
        db.commit()
        print("insert into success!")
        cursor.close()
        db.close()  # 关闭数据库的连接
    except:
        db.rollback()


def update_user(ip='localhost', usr='root', pwd='microsys', telephone="15244123456", password="12345678",
                passwd="12345678"):
    try:
        db = pymysql.connect(host=ip, user=usr, passwd=pwd, port=3306, charset='utf8', database='lawInfo')
        cursor = db.cursor()  # 创建游标对象
        print("connect is success!")
        sql_db = '''
                UPDATE user SET telephone='%s',password='%s',passwd='%s' WHERE telephone='%s';
        ''' % (telephone, password, passwd, telephone)
        print(sql_db)
        cursor.execute(sql_db)
        db.commit()
        cursor.close()
        db.close()  # 关闭数据库的连接
    except:
        print("错误：没有查找到数据")


def find_is_exist(ip='localhost', usr='root', pwd='microsys', account="anonymous", telephone="15244123456"):
    try:
        db = pymysql.connect(host=ip, user=usr, passwd=pwd, port=3306, charset='utf8', database='lawInfo')
        cursor = db.cursor()  # 创建游标对象
        print("connect is success!")
        sql_db = '''
                SELECT * FROM user WHERE account=('%s') OR telephone=('%s');
        ''' % (account, telephone)
        print(sql_db)
        cursor.execute(sql_db)
        results = cursor.fetchall()
        cursor.close()
        db.close()  # 关闭数据库的连接
        return results
    except:
        print("错误：没有查找到数据")


def find_user_id(ip='localhost', usr='root', pwd='microsys', account="anonymous"):
    try:
        db = pymysql.connect(host=ip, user=usr, passwd=pwd, port=3306, charset='utf8', database='lawInfo')
        cursor = db.cursor()  # 创建游标对象
        print("connect is success!")
        sql_db = '''
                SELECT id FROM user WHERE account='%s'
        ''' % (account)
        print(sql_db)
        cursor.execute(sql_db)
        id = cursor.fetchone()[0]
        cursor.close()
        db.close()  # 关闭数据库的连接
        return id
    except:
        print("错误：没有查找到数据")


def find_user(ip='localhost', usr='root', pwd='microsys', account="anonymous", password="12345678"):
    try:
        db = pymysql.connect(host=ip, user=usr, passwd=pwd, port=3306, charset='utf8', database='lawInfo')
        cursor = db.cursor()  # 创建游标对象
        print("connect is success!")
        sql_db = '''
                SELECT * FROM user WHERE (account=('%s') OR telephone=('%s')) AND password=('%s');
        ''' % (account, account, password)
        print(sql_db)
        cursor.execute(sql_db)
        results = cursor.fetchall()
        cursor.close()
        db.close()  # 关闭数据库的连接
        return results
    except:
        print("错误：没有查找到数据")


def insert_user(ip='localhost', usr='root', pwd='microsys', account="anonymous", password="12345678", passwd="12345678",
                telephone="15244123456"):
    try:
        db = pymysql.connect(host=ip, user=usr, passwd=pwd, port=3306, charset='utf8', database='lawInfo')
        cursor = db.cursor()  # 创建游标对象
        print("connect is success!")
        sql_db = '''
                INSERT IGNORE INTO user(account, password, passwd, telephone) VALUES('%s', '%s', '%s', '%s') 
                ON DUPLICATE KEY UPDATE telephone=VALUES(telephone);
        ''' % (account, password, passwd, telephone)
        print(sql_db)
        cursor.execute(sql_db)
        db.commit()
        print("insert into success!")
        cursor.close()
        db.close()  # 关闭数据库的连接
    except:
        db.rollback()


def insert_data(table_key, ip='localhost', usr='root', pwd='microsys'):
    try:
        db = pymysql.connect(host=ip, user=usr, passwd=pwd, port=3306, charset='utf8', database='lawInfo')
        cursor = db.cursor()  # 创建游标对象
        print("connect is success!")

        sql_db = f'''
                INSERT IGNORE INTO {table_key[0]}(title, content, link) VALUES(%s, %s, %s) ON DUPLICATE KEY UPDATE title=VALUES(title);
        '''
        # print(sql_db)
        values = CRAW.query_law_msg(table_key[1])
        cursor.executemany(sql_db, values)
        db.commit()
        print("insert into success!")
        cursor.close()
        db.close()  # 关闭数据库的连接
    except:
        db.rollback()


def rand_find_data(ip='localhost', usr='root', pwd='microsys', law_name='contractLaw'):
    try:
        db = pymysql.connect(host=ip, user=usr, passwd=pwd, port=3306, charset='utf8', database='lawInfo')
        cursor = db.cursor()  # 创建游标对象
        sql_db = f'''
                SELECT * FROM {law_name} AS t1 JOIN (SELECT ROUND(RAND() * ((SELECT MAX(id) FROM {law_name}) - (SELECT MIN(id)
                FROM {law_name}))+(SELECT MIN(id) FROM {law_name})) AS id from {law_name} limit 2) AS t2 on t1.id=t2.id
                ORDER BY t1.id;
        '''
        cursor.execute(sql_db)
        results = cursor.fetchall()
        cursor.close()
        db.close()  # 关闭数据库的连接
        return results
    except:
        print("错误：没有查找到数据")


def count_num(ip='localhost', usr='root', pwd='microsys', law_name='contractLaw'):
    try:
        db = pymysql.connect(host=ip, user=usr, passwd=pwd, port=3306, charset='utf8', database='lawInfo')
        cursor = db.cursor()  # 创建游标对象
        sql_db = f'''
                SELECT count(*) FROM {law_name};
        '''
        cursor.execute(sql_db)
        numbers = cursor.fetchone()[0]
        cursor.close()
        db.close()  # 关闭数据库的连接
        return numbers
    except:
        print("错误：没有查到统计总数")


def init_database(ip='localhost', usr='root', pwd='microsys'):
    create_database(ip=ip, usr=usr, pwd=pwd)
    insert_func = partial(insert_data, ip=ip, usr=usr, pwd=pwd)
    pool = Pool(5)
    pool.map(insert_func, zip(tables_list, keywords_list))


def multi_insert_data(ip='localhost', usr='root', pwd='microsys'):
    insert_func = partial(insert_data, ip=ip, usr=usr, pwd=pwd)
    pool = Pool(5)
    pool.map(insert_func, zip(tables_list, keywords_list))


if __name__ == '__main__':
    id = find_user_id(ip='localhost', usr='root', pwd='microsys', account="zjb_123")
    print(id)
#     db = pymysql.connect(host='localhost', user='root', passwd='microsys', port=3306, charset='utf8',
#                          database='lawInfo')
#     cursor = db.cursor()  # 创建游标对象
#     cursor.execute("select id from user where account='zjb_123';")
#     print(cursor.fetchone()[0])
#     print(find_user(account='15333333333', password='bobo@123456'))
#     rand_find_data()
#     sql = '''SELECT * FROM contractLaw AS t1 JOIN (SELECT ROUND(RAND() * ((SELECT MAX(id) FROM contractLaw) - (SELECT MIN(id)
#     FROM contractLaw))+(SELECT MIN(id) FROM contractLaw)) AS id from contractLaw limit 2) AS t2 on t1.id=t2.id
#     ORDER BY t1.id;
#     '''

# init_database()
# db = pymysql.connect(host='localhost', user='root', passwd='microsys', port=3306, charset='utf8', database='lawInfo')
# cursor = db.cursor()  # 创建游标对象
# print("connect is success!")
# cursor.execute(sql)
# result = cursor.fetchall()
# print(result)
#
# sql_db = f'''
#                 INSERT IGNORE INTO contractLaw(title, content, link) VALUES(%s, %s, %s);
#         '''
# print(sql_db)
# a = ('让法治成为最好的营商环境122', '\n\u3000\u3000一、证明原内地身份与现澳门身份“同', 'http://www.moj.gov.cn/pub/sfbgw/cszt/cszgflfwamgs/cszgwtgzfw/csbzzn/202211/t20221123_467885.html')
# cursor.execute(sql_db, a)
# print("insert into success")
# db.commit()
# cursor.close()
# db.close()
