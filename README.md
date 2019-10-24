# spiderNotices
爬取东方财富网站的公司公告列表及文本内容。

## 运行方法
- 1、本地安装mongodb数据库，python环境安装scrapy爬虫框架和requests等相关依赖。
- 2、设置项目spiderNotices.settings.REMOTEMONGO
    - 数据库的uri: REMOTEMONGO['uri']
    - 所在数据库名称：REMOTEMONGO['aiNotices']
- 3、项目运行，python 运行main.py脚本。或者切换到项目根目录，输入命令
```
scrapy crawl notices
```
- 4、运行结果：往数据库中存入数据，项目路径下生成log文件夹

## 数据调用
- spiderNotices.text_mongo.TextMongo对象的方法:
    - get_notices_stk::获取notices数据库下存在的表。
    - get_notices::从mongodb中获取数据。
    - get_notices_single::获取单个股票数据
    
```python
from spiderNotices.text_mongo import TextMongo
# 单个获取
result = TextMongo().get_notices_single('000001.SZ', '2010-01-01', '2012-12-31')
result = TextMongo().get_notices_single('000001.SZ')

# 多个获取
result = TextMongo().get_notices(['000001.SZ', '000002.SZ'])

# 遍历存有的股票
result = TextMongo().get_notices_stk()

```


## 爬虫设置
- settings.PAGE_SIZE:爬取第一页时的数据大小。
    - 首次运行，设置为None，会执行全部数据的爬取。
    - 往后增量更新，可以设为50或其它。
- DOWNLOADER_MIDDLEWARES可以启用`SeleniumMiddleware` `RandomUserAgent` `ProxyIpMiddleware`


## TODO
- [ ] pdf的文本提取和图片文字识别

- [ ] 市场新闻的爬取