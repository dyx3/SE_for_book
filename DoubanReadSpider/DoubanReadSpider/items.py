# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BookItem(scrapy.Item):
    # url
    url = scrapy.Field()
    # 书名
    name = scrapy.Field()
    # 作者
    author = scrapy.Field()
    # 出版社
    publisher = scrapy.Field()
    # 页数
    page_num = scrapy.Field()
    # 定价
    price = scrapy.Field()
    # 装帧
    binding = scrapy.Field()
    # 丛书
    series = scrapy.Field()
    # ISBN
    isbn = scrapy.Field()
    # 简介
    intro = scrapy.Field()
    # 评分
    score = scrapy.Field()
