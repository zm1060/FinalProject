# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html
import random

from scrapy import signals
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from w3lib.http import basic_auth_header

from app import credentials
from jdspider import settings
from jdspider.useragents import USER_AGENTS


class JdspiderSpiderMiddleware(object):
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

        # Should return either None or an iterable of Response, dict
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


class UserAgentmiddleware(UserAgentMiddleware):
    def process_request(self, request, spider):
        agent = random.choice(USER_AGENTS)
        # log.msg('agent : %s' % agent,level=log.INFO)
        request.headers['User-Agent'] = agent


from scrapy.mail import MailSender

class EmailNotificationMiddleware(object):
    def __init__(self, settings):
        self.mailer = MailSender.from_settings(settings)

    def process_spider_exception(self, response, exception, spider):
        self.send_email_notification(exception)

    def send_email_notification(self, exception):
        subject = 'Scrapy notification'
        body = str(exception)
        self.mailer.send(to=settings.get('MAIL_RECIPIENTS'), subject=subject, body=body)



class ProxyDownloaderMiddleware:
    url = credentials.proxy
    port = credentials.port
    _proxy = (url, port)

    def process_request(self, request, spider):

        # 用户名密码认证
        username = credentials.username
        password = credentials.password
        request.meta['proxy'] = "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": ':'.join(ProxyDownloaderMiddleware._proxy)}

        # 白名单认证
        # request.meta['proxy'] = "http://%(proxy)s/" % {"proxy": proxy}

        request.headers["Connection"] = "close"
        return None

    def process_exception(self, request, exception, spider):
        """捕获407异常"""
        if "'status': 407" in exception.__str__():  # 不同版本的exception的写法可能不一样，可以debug出当前版本的exception再修改条件
            from scrapy.resolver import dnscache
            dnscache.__delitem__(ProxyDownloaderMiddleware._proxy[0])  # 删除proxy host的dns缓存
        return exception