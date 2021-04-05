# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3


# from .preprocessing.process import process


class TutorialPipeline:

    def __init__(self):
        self.conn = sqlite3.connect('test.db')
        self.c = self.conn.cursor()
        sqlstate = "drop table if exists books"
        self.c.execute(sqlstate)

        sqlstate = """create table if not exists books(
        bookid int primary key not null,
        name nvarchar(50),
        author nvarchar(50),
        publisher nvarchar(50),
        subtitle nvarchar(50),
        date nvarchar(50),
        price nvarchar(50),
        bookintro nvarchar(500),
        score decimal(3,1),
        commentNum int,
        tag nvarchar(50),
        short_comment1 nvarchar(500),
        short_comment2 nvarchar(500),
        comment1 nvarchar(10000),
        features1 nvarchar(500),
        comment2 nvarchar(10000),
        features2 nvarchar(500)
        )
        """
        self.c.execute(sqlstate)
        self.conn.commit()

    def process_item(self, item, spider):
        # sqlstate = """insert into books values(%d,'%s','%s','%s','%s','%s','%s','%s',%s,%s,'%s','%s','%s','%s','%s','%s','%s')""" % (
        #     item['bookid'], item['name'], item['author'], item['publisher'], item['subtitle'], item['date'],
        #     item['price'], item['bookintro'], item['score'][0], item['commentNum'][0],
        #     item['tag'], item['short_comment1'], item['short_comment2'],
        #     item['comment1'].replace('\\', '\\\''), item['features1'], item['comment2'].replace('\\', '\\\''),
        #     item['features2'])
        # # print(sqlstate)
        # self.c.execute(sqlstate)
        sqlstate = "insert into books values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
        self.c.execute(sqlstate,( item['bookid'], item['name'], item['author'], item['publisher'], item['subtitle'], item['date'],
            item['price'], item['bookintro'], item['score'][0], item['commentNum'][0],
            item['tag'], item['short_comment1'], item['short_comment2'],
            item['comment1'].replace('\\', '\\\''), item['features1'], item['comment2'].replace('\\', '\\\''),
            item['features2']))
        self.conn.commit()
        return item

    def __del__(self):
        # process()
        self.conn.close()
