# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

import random
from logging import getLogger
from scrapy import signals
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from scrapy.http import HtmlResponse

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests

from .utils import user_agent_list


class SpidernoticesSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class SpidernoticesDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class SeleniumMiddleware(object):
    """
    使用Selenium加载动态页面。
    1、process_request:通过request.url判断。

    """

    def __init__(self, timeout=10, service_args=[]):
        self.logger = getLogger(__name__)

        self.browser = webdriver.PhantomJS(service_args=service_args)
        self.timeout = timeout
        self.wait = WebDriverWait(self.browser, self.timeout)

    def __del__(self):
        self.browser.close()

    def process_request(self, request, spider):
        if request.url.find(r'data.eastmoney.com/notices/stock/') != -1:
            # 个股公告公告列表，此时AJX加载到第一页
            self.logger.debug('Selenium is Starting')
            try:
                self.browser.get(request.url)
                # time.sleep(3)
                self.wait.until(
                    EC.presence_of_element_located((By.ID, 'PageCont'))
                )
                return HtmlResponse(url=request.url, body=self.browser.page_source, request=request, encoding='utf-8',
                                    )
            except TimeoutException:
                return HtmlResponse(url=request.url, status=500, request=request)
        else:
            return None


class ProxyIpMiddleware(object):
    """
    使用ip:port格式的代理。从127.0.0.1:5010构建的项目'proxy_pool'中获取
    """
    server_uri = 'http://127.0.0.1:5010'
    test_web = 'https://data.eastmoney.com'
    logger = getLogger(__name__)

    def process_request(self, request, spider):
        try:
            proxy = self._get_proxy(request.url)
        except Exception as e:
            self.logger.warning('获取代理失败{}'.format(e))
            return
        else:
            if proxy:
                request.meta["proxy"] = "http://" + proxy

    def _get_proxy(self, uri):
        proxy = requests.get(self.server_uri + "/get/").json().get('proxy')
        if self._check_uri(proxy, uri):
            return proxy
        else:
            return None

    def _delete_proxy(self, proxy):
        requests.get(self.server_uri+"/delete/?proxy={}".format(proxy))

    def _check_uri(self, proxy, uri):
        retry_count = 5
        while retry_count > 0:
            try:
                html = requests.get(uri, proxies={"http": "http://{}".format(proxy)})
                if html.status_code == 200:
                    return True
            except Exception:
                retry_count -= 1
        # 出错5次, 删除代理池中代理
        self.logger.warning('不适用代理{}'.format(uri))
        self._delete_proxy(proxy)
        return False


class RandomUserAgent(UserAgentMiddleware):
    """
    随机设置一个useragent
    """

    def process_request(self, request, spider):
        ua = random.choice(user_agent_list)
        request.headers.setdefault('User-Agent', ua)