# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BookDoubanItem(scrapy.Item):
    # Ψһ bookid
    bookid = scrapy.Field()
    # ����
    name = scrapy.Field()
    # ������
    subtitle = scrapy.Field()
    # ��������
    date = scrapy.Field()
    # �۸�
    price = scrapy.Field()
    # ����
    author = scrapy.Field()
    # ������
    publisher = scrapy.Field()
    # ���
    bookintro = scrapy.Field()
    # ��������
    score = scrapy.Field()
    # ������
    commentNum = scrapy.Field()
    # ��ǩ
    tag = scrapy.Field()
    # ����1
    comment1 = scrapy.Field()
    # ����2
    comment2 = scrapy.Field()
    # ����1
    short_comment1 = scrapy.Field()
    # ����2
    short_comment2 = scrapy.Field()
    # ��һ��������ȡ��������
    features1 = scrapy.Field()
    # �ڶ���������ȡ��������
    features2 = scrapy.Field()
