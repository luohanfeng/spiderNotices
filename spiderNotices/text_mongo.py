"""
mongodb中的文本数据。

"""
import pandas as pd
from dateutil.parser import parse
from pymongo import MongoClient

from spiderNotices.settings import REMOTEMONGO


class TextMongo(object):
    """" 只做数据查询。"""

    def __init__(self, uri=REMOTEMONGO['uri']):
        self.client = MongoClient(uri)
        # 上市公司公告的数据库
        self.db_notices = self.client[REMOTEMONGO['notices']]

    def get_notices_stk(self):
        """ 获取notices数据库下存在的表。"""
        coll_names = self.db_notices.list_collection_names(session=None)
        coll_names.sort()
        return coll_names

    def get_notices(self, stk_list=[], begin='', end='', columns=[]):
        """
        从mongodb中获取数据。
        :param stk_list: xxxxxx.zz或xxxxxx.zzzz格式，切分后取前面数字编码。
        :param begin:
        :param end:
        :param columns:
        :return: DataFrame
        """
        # 循环股票列表
        stk_list = list(set(stk_list))
        stk_list.sort()
        each_list = []
        for stk in stk_list:
            each = self.get_notices_single(stk, begin=begin, end=end, columns=columns)
            if not each.empty:
                each_list.append(each)
        df = pd.concat(each_list).reset_index(drop=True)
        return df

    def get_notices_single(self, stk, begin='', end='', columns=[]):
        # 数据库表
        coll = self.db_notices[stk.split('.')[0]]

        # 查询条件
        query = {}
        if begin:
            begin = parse(begin)
            if end:
                end = parse(end)
                query['ann_date'] = {"$gte": begin, "$lte": end}
            else:
                query['ann_date'] = {"$gte": begin}
        else:
            if end:
                end = parse(end)
                query['ann_date'] = {"$lte": end}
            else:
                pass

        # 查询列
        if columns:
            cursor = coll.find(query, {x: 1 for x in columns})  # query为{}时，全取出
        else:
            cursor = coll.find(query)
        df = pd.DataFrame(list(cursor))

        # 整理数据
        if '_id' in df.columns:
            del df['_id']
        df.reset_index(drop=True, inplace=True)

        return df


if __name__ == '__main__':
    # 单个获取
    result = TextMongo().get_notices_single('000001.SZ', '2010-01-01', '2012-12-31')
    result = TextMongo().get_notices_single('000001.SZ')

    # 多个获取
    result = TextMongo().get_notices(['000001.SZ', '000002.SZ'])

    # 遍历存有的股票
    result = TextMongo().get_notices_stk()
