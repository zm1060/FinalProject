#!/usr/bin/env python
# encoding: utf-8
import requests

from weibospider import settings


class IPProxyMiddleware(object):
    """
    代理IP中间件
    """

    @staticmethod
    def fetch_proxy():
        """
        获取一个代理IP
        """
        # api_url = 'https://your-api-url.com/proxies'
        # response = requests.get(api_url)
        # if response.status_code == 200:
        #     proxy_data = response.json().get('proxy')
        #     if proxy_data:
        #         return proxy_data
        return None

    def process_request(self, request, spider):
        """
        将代理IP添加到request请求中
        """
        proxy_data = self.fetch_proxy()
        if proxy_data:
            current_proxy = f'http://{proxy_data}'
            spider.logger.debug(f"current proxy:{current_proxy}")
            request.meta['proxy'] = current_proxy


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
    _proxy = ('f675.kdltps.com', '15818')

    def process_request(self, request, spider):

        # 用户名密码认证
        username = "t18290722811974"
        password = "so4zel3m"
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