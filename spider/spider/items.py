# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BookDoubanItem(scrapy.Item):
    # 唯一 bookid
    bookid = scrapy.Field()
    # 书名
    name = scrapy.Field()
    # 副标题
    subtitle = scrapy.Field()
    # 出版日期
    date = scrapy.Field()
    # 价格
    price = scrapy.Field()
    # 作者
    author = scrapy.Field()
    # 出版社
    publisher = scrapy.Field()
    # 简介
    bookintro = scrapy.Field()
    # 豆瓣评分
    score = scrapy.Field()
    # 评论数
    commentNum = scrapy.Field()
    # 标签
    tag = scrapy.Field()
    # 长评1
    comment1 = scrapy.Field()
    # 长评2
    comment2 = scrapy.Field()
    # 短评1
    short_comment1 = scrapy.Field()
    # 短评2
    short_comment2 = scrapy.Field()
    # 第一条长评提取出的特征
    features1 = scrapy.Field()
    # 第二条长评提取出的特征
    features2 = scrapy.Field()
