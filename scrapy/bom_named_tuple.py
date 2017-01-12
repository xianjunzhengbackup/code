from scrapy import signals
from scrapy.conf import settings
from scrapy.crawler import CrawlerProcess
from scrapy.xlib.pydispatch import dispatcher
from multiprocessing.queues import Queue
import scrapy
import multiprocessing
import datetime

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
        
class CanberraWealtherSpider(scrapy.Spider):
    name = "CanberraWealtherSpider"
    allowed_domains = ["www.bom.gov.au"]
    start_urls = ['http://www.bom.gov.au/act/forecasts/canberra.shtml']

    def parse(self, response):
        Max_Temperatures=response.xpath('//em[@class="max"]/text()').extract()
        for temperature in Max_Temperatures:
            yield {"Max_Temperature":temperature.encode('utf-8')}
            
        Min_Temperatures=response.xpath('//em[@class="min"]/text()').extract()
        for temperature in Min_Temperatures:
            yield {"Min_Temperature":temperature.encode('utf-8')}
            
        Summarys=response.xpath('//dd[@class="summary"]/text()').extract()
        for summary in Summarys:
            yield {"summary":summary.encode('utf-8')}
            
            
            
def main():
    result_queue = Queue()
    crawler = CrawlerWorker(CanberraWealtherSpider(), result_queue)
    crawler.start()
    for item in result_queue.get():
        print datetime.datetime.now(),item
        
if __name__=="__main__":
    main()