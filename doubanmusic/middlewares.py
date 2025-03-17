# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

import random

from scrapy import signals
from .utils.entity import get_user_agent

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter

# TODO 设置代理IP
import logging
import requests

# 配置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ProxyMiddleware:
    def __init__(self):
        # 初始化隧道代理的用户名、密码和地址
        self.tunnel_username = 't14186799080081'
        self.tunnel_password = 'w7xvgxeb'
        self.tunnel = 'i528.kdltps.com:15818'
        # 生成代理的 URL 格式
        self.proxy_url = f"http://{self.tunnel_username}:{self.tunnel_password}@{self.tunnel}"

    def process_request(self, request, spider):
        try:
            # 为请求设置代理
            request.meta['proxy'] = self.proxy_url
            logging.info(f"Set proxy {self.proxy_url} for request: {request.url}")

            # 可添加代理可用性检查
            # test_url = 'http://httpbin.org/ip'
            # response = requests.get(test_url, proxies={"http": self.proxy_url, "https": self.proxy_url}, timeout=5)
            # if response.status_code == 200:
            #     logging.info(f"Proxy {self.proxy_url} is available.")
            # else:
            #     logging.warning(f"Proxy {self.proxy_url} returned status code {response.status_code}.")
        except Exception as e:
            # 处理异常，记录错误信息
            logging.error(f"Error setting proxy for request {request.url}: {e}")

# TODO 设置User-Agent
class UserAgentMiddleware:

    def process_request(self, request, spider):
        user_agent = get_user_agent()
        request.headers['User-Agent'] = user_agent



class DoubanmusicSpiderMiddleware:
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

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class DoubanmusicDownloaderMiddleware:
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
        spider.logger.info("Spider opened: %s" % spider.name)
