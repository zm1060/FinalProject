import os

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from jdspider.spiders.JDspider import JDspider


def run_spider_directly(search_name=None):
    task_id = "direct_run"
    spider_kwargs = {
        'search_name': search_name,
        'task_id': task_id
    }
    os.environ['SCRAPY_SETTINGS_MODULE'] = 'jdspider.settings'
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    process.crawl(JDspider, **spider_kwargs)
    process.start()


run_spider_directly(search_name="iphone")
