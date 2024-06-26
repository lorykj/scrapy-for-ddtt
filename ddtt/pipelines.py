# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os
from datetime import datetime

import pymssql
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import os
import codecs
import json


class DdttPipeline:
    # def process_item(self, item, spider):
    #     return item
    # 打开文件
    # def open_spider(self, spider):
    #     print("==========================开始爬取电影========================")
    #     self.fp = open("movies.json", "w", encoding="utf-8")
    #
    # # 写入数据
    # def process_item(self, item, spider):
    #     self.fp.write(str(item))
    #     return item
    #
    # # 关闭文件
    # def close_spider(self, spider):
    #     self.fp.close()
    #     print("============================爬取结束=========================")
    # 构造方法（初始化对象时执行的方法）
    def __init__(self):
        # 必须使用 w+ 模式打开文件，以便后续进行 读写操作（w+模式，意味既可读，亦可写）
        # 注意：此处打开文件使用的不是 python 的 open 方法，而是 codecs 中的 open 方法
        self.json_file = codecs.open('data.json', 'w+', encoding='UTF-8')

    # 爬虫开始时执行的方法
    def open_spider(self, spider):
        # 在爬虫开始时，首先写入一个 '[' 符号，构造一个 json 数组
        # 为使得 Json 文件具有更高的易读性，我们辅助输出了 '\n'（换行符）
        self.json_file.write('[\n')

    # 爬虫 pipeline 接收到 Scrapy 引擎发来的 item 数据时，执行的方法
    def process_item(self, item, spider):
        # 将 item 转换为 字典类型，并编码为 json 字符串，写入文件
        # 为使得 Json 文件具有更高的易读性，我们辅助输出了 '\t'（制表符） 与 '\n'（换行符）
        print("==========================开始爬取电影========================")
        item_json = json.dumps(dict(item), ensure_ascii=False)
        self.json_file.write('\t' + item_json + ',\n')
        return item

    # 爬虫结束时执行的方法
    def close_spider(self, spider):
        # 在结束后，需要对 process_item 最后一次执行输出的 “逗号” 去除
        # 当前文件指针处于文件尾，我们需要首先使用 SEEK 方法，定位文件尾前的两个字符（一个','(逗号), 一个'\n'(换行符)）的位置
        self.json_file.seek(-2, os.SEEK_END)
        # 使用 truncate() 方法，将后面的数据清空
        self.json_file.truncate()
        # 重新输出'\n'，并输入']'，与 open_spider(self, spider) 时输出的 '['，构成一个完整的数组格式
        self.json_file.write('\n]')
        # 关闭文件
        self.json_file.close()
        print("============================爬取结束=========================")

# class MysqlPipeline:
#     def open_spider(self, spider):
#         print("==========================开始写入数据========================")
#         self.connect()
#
#     def connect(self):
#         server = '(local)'
#         database = 'MovieDB'
#         username = 'sa'
#         password = 'lkj183495'
#         # 连接到数据库
#         self.conn = pymssql.connect(server=server, user=username, password=password, database=database)
#         self.cur = self.conn.cursor()
#
#     def process_item(self, item, spider):
#         name = item['name']
#         year = item['year']
#         src = item['src']
#         area = item['area']
#         genre = item['genre']
#         language = item['language']
#         vote = item['vote']
#         vote_cnt = item['vote_cnt']
#         actor = item['actor']
#         director = item['director']
#         runtime = item['runtime']
#         print(name, year, area, genre, vote)
#         date_str = item['date']
#         # 提交sql语句
#         sql = f"insert into [Movie] values('{name}', {year}, '{area}', '{genre}', {vote}, '{src}')"
#
#         sql2 = f"insert into [Info] values('{name}', '{date_str}', '{language}', {vote_cnt}, {runtime}, '{director}', '{actor}', '')"
#
#         try:
#             self.cur.execute(sql, (name, year, area, genre, vote, src))
#             self.conn.commit()
#             print("插入成功1")
#         except Exception as e:
#             print("插入失败1:", e)
#
#         try:
#             self.cur.execute(sql2, (name, date_str, language, vote_cnt, runtime, director, actor, ""))
#             self.conn.commit()
#             print("插入成功2")
#         except Exception as e:
#             print("插入失败2:", e)
#         return item
#
#     # 关闭数据库连接
#     def close_spider(self, spider):
#         self.cur.close()
#         self.conn.close()
#         print("==========================写入完成========================")
#
#
# import urllib.request
#
#
# # 第二条管道，可以实现同时进行多条管道的处理
# class MovieDownloadPipeline:
#     def process_item(self, item, spider):
#         print("==========================开始下载========================")
#         url = item.get('src')
#         filename = "./ddtt/" + item.get('name') + ".jpg"
#         urllib.request.urlretrieve(url=url, filename=filename)
#         # 检查文件是否已经存在
#         if not os.path.exists(filename):
#             urllib.request.urlretrieve(url=url, filename=filename)
#             print("文件下载成功:", filename)
#         else:
#             print("文件已存在，跳过下载:", filename)
#         return item
