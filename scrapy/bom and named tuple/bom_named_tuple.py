
# coding: utf-8

# In[10]:

from scrapy import signals
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess
from scrapy.xlib.pydispatch import dispatcher
from multiprocessing.queues import Queue
import scrapy
import multiprocessing
import datetime
import collections


# In[31]:

wealther_data=collections.namedtuple('wealther_data','day,max_t,min_t,summary')


# In[32]:

class CrawlerWorker(multiprocessing.Process):

    def __init__(self, spider, result_queue):
        multiprocessing.Process.__init__(self)
        self.result_queue = result_queue

        self.crawler = CrawlerProcess(get_project_settings())
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
        


# In[36]:

class CanberraWealtherSpider(scrapy.Spider):
    name = "CanberraWealtherSpider"
    allowed_domains = ["www.bom.gov.au"]
    start_urls = ['http://www.bom.gov.au/act/forecasts/canberra.shtml']

    def parse(self, response):
        forecast_tags=response.xpath('//div[@class="forecast"]')
        i=0
        today=datetime.datetime.today()
        for forecast_eachday in forecast_tags:
#注意这里子tag的写法，它是绝对路径。如果写成相对路径，forecast_eachday.xpath('//em[@class="max"]/text()').extract()
#会出错。比如运行forecast_tags[0].xpath('//em[@class="max"]/text()').extract(),结果将是forecast_tag[0]-forecast_tag[6]七个
#关于max的结果。所以子路径这里一定要用绝对路径
            Max_Temperature=forecast_eachday.xpath('dl/dd/em[@class="max"]/text()').extract()
            Min_Temperature=forecast_eachday.xpath('dl/dd/em[@class="min"]/text()').extract()
            if Min_Temperature == []:
                Min_Temperature=['Not Exist']
            Summary=forecast_eachday.xpath('dl/dd[@class="summary"]/text()').extract()
            date=today+datetime.timedelta(i)
            i = i+1
            wealther=wealther_data(str(date.date()),Max_Temperature[0].encode('utf-8'),Min_Temperature[0].encode('utf-8'),Summary[0].encode('utf-8'))
            yield {str(date.date()):wealther}
            #yield wealther_data(str(date.date()),Max_Temperature[0].encode('utf-8'),Min_Temperature[0].encode('utf-8'),Summary[0].encode('utf-8'))
            #yield{'max':Max_Temperature[0].encode('utf-8'),'min':Min_Temperature[0].encode('utf-8'),'summary':Summary[0].encode('utf-8')}


# In[37]:

def main():
    result_queue = Queue()
    crawler = CrawlerWorker(CanberraWealtherSpider(), result_queue)
    crawler.start()
    for item in result_queue.get():
        #print datetime.datetime.now(),item
        print item


# In[38]:

if __name__ == '__main__':
    main()


# In[ ]:



