#!/usr/bin/env python
# encoding: utf-8
import requests

class IPProxyMiddleware(object):
    """
    代理IP中间件
    """

    @staticmethod
    def fetch_proxy():
        """
        获取一个代理IP
        """
        api_url = 'https://your-api-url.com/proxies'
        response = requests.get(api_url)
        if response.status_code == 200:
            proxy_data = response.json().get('proxy')
            if proxy_data:
                return proxy_data
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
