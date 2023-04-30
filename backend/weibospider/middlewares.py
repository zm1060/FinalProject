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
