# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
from dateutil.parser import parse
import hashlib


class SpidernoticesPipeline(object):
    def process_item(self, item, spider):
        return item


class ItemToMongo(object):

    def __init__(self, uri, db_name):
        self.client = MongoClient(uri)
        self.db_name = db_name

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            uri=crawler.settings.get('REMOTEMONGO')['uri'],
            db_name=crawler.settings.get('REMOTEMONGO')['notices']
        )

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        """ 存储到mongodb，数据库aiStkNotices
        一个股票对应一张表，表名只有xxxxxx六位证券代码。

        """
        post = dict(item)
        coll = self.client[self.db_name][post['code']]

        temp = parse(post['ann_date']).strftime('%Y-%m-%d')  # 网站上显示的只有前面的日期，不考虑tzone
        post['ann_date'] = parse(temp)
        post['_id'] = hashlib.md5(post['href'].encode('utf8')).hexdigest()
        # coll.insert_one(post)  # 有值再插入pymongo.errors.DuplicateKeyError
        coll.update_one({'_id': post.pop('_id')}, {'$set': post}, upsert=True)

        return item