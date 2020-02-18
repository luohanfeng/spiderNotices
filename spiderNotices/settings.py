# -*- coding: utf-8 -*-
import os
import datetime


# TODO log分析，完善爬取自动化


# 一页数据量
PAGE_SIZE = None

# 远程数据库
REMOTEMONGO = {
    # 'uri': 'mongodb://read:read123456@120.92.189.17:27027',  # /?authSource=amdin&authMechanism=SCRAM-SHA-1
    #            'host': '120.92.189.17',
    #            'port': 27027,
    'uri': 'mongodb://hfam:hfam5714@127.0.0.1:27017',  # 本地配置
    'host': '127.0.0.1',
    'port': 27017,

    'username': 'hfam',
    'password': 'hfam5714',
    'notices': 'aiNotices',
}

# --------------------------------------------------------------------------------------------
# Scrapy settings for spiderNotices project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'spiderNotices'

SPIDER_MODULES = ['spiderNotices.spiders']
NEWSPIDER_MODULE = 'spiderNotices.spiders'

DOWNLOAD_TIMEOUT = 120  # 下载超时时间
RETRY_ENABLED = True  # 打开重试开关
RETRY_TIMES = 5  # 重试次数
RETRY_HTTP_CODES = [429,404,403,400]  # 重试

today = datetime.datetime.now()
SETTINGS_PATH = os.path.abspath(__file__)
LOG_FILE = os.path.join(os.path.dirname(SETTINGS_PATH), f'log/{today.year}_{today.month}_{today.day}.log')
LOG_LEVEL = 'WARNING'
# LOG_LEVEL = 'INFO'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'spiderNotices (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 10
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'spiderNotices.middlewares.SpidernoticesSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    # 'spiderNotices.middlewares.SpidernoticesDownloaderMiddleware': 543,
    #  'spiderNotices.middlewares.SeleniumMiddleware': 100,
    'spiderNotices.middlewares.RandomUserAgent': 200,
    'spiderNotices.middlewares.ProxyIpMiddleware': 201,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    # 'spiderNotices.pipelines.SpidernoticesPipeline': 300,
    'spiderNotices.pipelines.ItemToMongo': 400,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
