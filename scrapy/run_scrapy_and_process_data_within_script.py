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
        
class chnausSpider(scrapy.Spider):
    name = "chnausSpider"
    allowed_domains = ["www.chnaus.com.au"]
    start_urls = ['http://www.chnaus.com/forum-house-1.html']

    def parse(self, response):
        a_tags=response.xpath('//a[contains(@href,"www.chnaus.com") and @onclick="atarget(this)"]')
        for a in a_tags:
            title=a.xpath('text()').extract()[0]
            link=a.xpath('@href').extract()[0]
            yield {'title':title,'link':link}
 
def main():
    result_queue = Queue()
    crawler = CrawlerWorker(chnausSpider(), result_queue)
    crawler.start()
    for item in result_queue.get():
        print datetime.datetime.now(),item
        
if __name__=="__main__":
    main()
#这个就解决了不用建立scrapy工程，同样可以调用scrapy，同时又可以得到爬下来的数据
#the main reason for 'if __name__=="__main__"' is for unit testing,
#from run_scrapy_and_process_data_within_script import main as func1
#func1 