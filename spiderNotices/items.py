# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SpidernoticesItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class NoticeItem(scrapy.Item):
    code = scrapy.Field()  # 证券代码xxxxxx六位数字

    ann_date = scrapy.Field()  # 公告日期
    ann_title = scrapy.Field()
    ann_type = scrapy.Field()

    href = scrapy.Field()
    href_md5 = scrapy.Field()
    content = scrapy.Field()
    content_source = scrapy.Field()  # 公告内容来源，0 空，1 网页text， 2 pdf解析
