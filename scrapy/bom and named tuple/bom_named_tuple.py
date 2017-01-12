
# coding: utf-8

# In[1]:

from scrapy import signals
from scrapy.conf import settings
from scrapy.crawler import CrawlerProcess
from scrapy.xlib.pydispatch import dispatcher
from multiprocessing.queues import Queue
import scrapy
import multiprocessing
import datetime


# In[2]:

class CrawlerWorker(multiprocessing.Process):

    def __init__(self, spider, result_queue):
        multiprocessing.Process.__init__(self)
        self.result_queue = result_queue

        self.crawler = CrawlerProcess(settings)
        #if not hasattr(project, 'crawler'):
        #    self.crawler.install()
        #self.crawler.configure()

        self.items = []
        self.spider = spider
        dispatcher.connect(self._item_passed, signals.item_passed)

    def _item_passed(self, item):
        self.items.append(item)

    def run(self):
        self.crawler.crawl(self.spider)
        self.crawler.start()
        self.crawler.stop()
        self.result_queue.put(self.items)
        


# In[22]:

class CanberraWealtherSpider(scrapy.Spider):
    name = "CanberraWealtherSpider"
    allowed_domains = ["www.bom.gov.au"]
    start_urls = ['http://www.bom.gov.au/act/forecasts/canberra.shtml']

    def parse(self, response):
        forecast_tags=response.xpath('//div[@class="forecast"]')
#注意这里子tag的写法，它是绝对路径。如果写成相对路径，forecast_eachday.xpath('//em[@class="max"]/text()').extract()
#会出错。比如运行forecast_tags[0].xpath('//em[@class="max"]/text()').extract(),结果将是forecast_tag[0]-forecast_tag[6]七个
#关于max的结果。所以子路径这里一定要用绝对路径。
        for forecast_eachday in forecast_tags:
            Max_Temperature=forecast_eachday.xpath('dl/dd/em[@class="max"]/text()').extract()
            Min_Temperature=forecast_eachday.xpath('dl/dd/em[@class="min"]/text()').extract()
            if Min_Temperature == []:
                Min_Temperature=['Not Exist']
            Summary=forecast_eachday.xpath('dl/dd[@class="summary"]/text()').extract()
            yield{'max':Max_Temperature[0].encode('utf-8'),'min':Min_Temperature[0].encode('utf-8'),'summary':Summary[0].encode('utf-8')}


# In[23]:

def main():
    result_queue = Queue()
    crawler = CrawlerWorker(CanberraWealtherSpider(), result_queue)
    crawler.start()
    for item in result_queue.get():
        #print datetime.datetime.now(),item
        print item


# In[24]:

if __name__ == '__main__':
    main()


# In[ ]:



