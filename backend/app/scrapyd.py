from scrapyd_api import ScrapydAPI

def deploy_spider(project_name, spider_name):
    # connect to Scrapyd server
    scrapyd = ScrapydAPI('http://localhost:6800')

    # deploy spider
    result = scrapyd.schedule(project_name, 'default', spider_name)

    return result