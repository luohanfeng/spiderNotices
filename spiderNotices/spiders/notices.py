# -*- coding: utf-8 -*-
import scrapy
import tushare as ts
import urllib
import copy
import requests
from pymongo import MongoClient
import re
import hashlib
from spiderNotices.items import NoticeItem
from spiderNotices.text_mongo import TextMongo
from spiderNotices.utils import ashx_json


class NoticesSpider(scrapy.Spider):
    name = 'notices'
    allowed_domains = ['eastmoney.com']
    start_urls = ['http://eastmoney.com/']

    # 股票列表
    shangshi = list(ts.pro_api().stock_basic(list_status='L')['ts_code'].drop_duplicates())
    tuishi = list(ts.pro_api().stock_basic(list_status='D')['ts_code'].drop_duplicates())
    zanting = list(ts.pro_api().stock_basic(list_status='P')['ts_code'].drop_duplicates())
    ts_code_list = list(set(shangshi + tuishi + zanting))
    code_list = [x.split('.')[0] for x in ts_code_list]
    code_list.sort()
    # code_list = ['000001', '000002']

    url_ashx = "http://data.eastmoney.com/notices/getdata.ashx"

    # 对应数据库
    db = None

    def start_requests(self):
        """"
        第一次请求数据。指定page_size，若未指定则请求该股票所有数据。
        """

        self.db = MongoClient(self.settings.get('REMOTEMONGO')['uri'])[self.settings.get('REMOTEMONGO')['notices']]
        if self.settings.get('PAGE_SIZE'):
            to_parse = self.code_list
            self.logger.info('增量更新：PAGE_SIZE{},to_parse数量{}'.format(self.settings.get('PAGE_SIZE'), len(to_parse)))

            for stk in to_parse:
                item = NoticeItem()
                item['code'] = stk
                params = {
                    'StockCode': stk,
                    'CodeType': 1,
                    'PageIndex': 1,
                    'PageSize': self.settings.get('PAGE_SIZE'),
                }
                url = self.url_ashx + '?' + urllib.parse.urlencode(params)
                yield scrapy.Request(
                    url=url, callback=self.parse, meta={'item': copy.deepcopy(item)}
                )
        else:
            existed = TextMongo().get_notices_stk()
            to_parse = list(set(self.code_list).difference(set(existed)))
            to_parse.sort()
            self.logger.info('剩余量更新：PAGE_SIZE为None,to_parse数量{}'.format(len(to_parse)))

            for stk in to_parse:
                item = NoticeItem()
                item['code'] = stk
                params = {
                    'StockCode': stk,
                    'CodeType': 1,
                    'PageIndex': 1,  # 证券市场，hsa为1，必须要有，否则TotalCount会出问题。
                    'PageSize': 50,
                }
                url = self.url_ashx + '?' + urllib.parse.urlencode(params)
                first = requests.get(url)
                page_size = ashx_json(first.text)['TotalCount']
                self.logger.warning('{}数据总数{}'.format(item['code'], page_size))
                if page_size == 0:  # 有些证券，网站没有数据。page_size为0，parse函数中会报错，所以眺过
                    continue

                params = {
                    'StockCode': stk,
                    'CodeType': 1,
                    'PageIndex': 1,
                    'PageSize': page_size,
                }
                url = self.url_ashx + '?' + urllib.parse.urlencode(params)
                yield scrapy.Request(
                    url=url, callback=self.parse, meta={'item': copy.deepcopy(item)}
                )

    def parse(self, response):
        """
        分析返回的数据结构，获取公告的摘要信息。
        """
        item = response.meta['item']
        assert item['code'] == re.findall(r'StockCode=(.*?)&', response.url)[0]

        # 已存在的数据，且content不为空。
        # TODO 按需设置有效数据的规则，例如pdf处理
        # exsit_md5 = self.db[item['code']].find({'content_source': {'$ne': 0}}, {'_id': 1, 'href_md5': 1})
        exsit_md5 = self.db[item['code']].find({'content_source': {'$in': [0, 1]}}, {'_id': 1, 'href_md5': 1})
        exsit_md5 = [x.get('href_md5') for x in exsit_md5]

        total = ashx_json(response.body_as_unicode())
        for each in total.get('data'):
            item['ann_date'] = each.get('NOTICEDATE')
            item['ann_title'] = each.get('NOTICETITLE')
            item['ann_type'] = each.get('ANN_RELCOLUMNS')[0].get('COLUMNNAME')  # 有些type不属于公告分类table，而是'其它' '股票'这种字段
            item['href'] = each.get('Url')
            item['href_md5'] = hashlib.md5(item['href'].encode('utf8')).hexdigest()
            if item['href_md5'] in exsit_md5:
                continue

            copy_item = copy.deepcopy(item)
            yield scrapy.Request(
                copy_item['href'], callback=self.parse_content, meta={'item': copy_item}
            )

    def parse_content(self, response):
        """ 获取公告对应的文本内容。"""
        item = response.meta['item']
        try:
            temp = response.xpath("//div[@class='detail-body']/div/text()").extract()
            temp = [x for x in temp if str(x).strip()]
            temp = '\r\n'.join(temp)
            item['content'] = temp
            item['content_source'] = 1
        except Exception as e:
            self.logger.warning('链接文本为空{}'.format(item['href']))  # TODO 做pdf的提取
            item['content'] = ''
            item['content_source'] = 0

        return item
