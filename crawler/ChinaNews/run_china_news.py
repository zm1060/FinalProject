import subprocess

def run_scrapy_spider():
    spider_name = 'chinanews'
    cmd = ['scrapy', 'crawl', spider_name]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()
    return out.decode('utf-8'), err.decode('utf-8')