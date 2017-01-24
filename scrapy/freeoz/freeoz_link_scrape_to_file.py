
# coding: utf-8

# In[33]:

from scrapy import signals
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess
from scrapy.xlib.pydispatch import dispatcher
from multiprocessing.queues import Queue
import scrapy
import multiprocessing
import urllib
from scrapy import Request as Request


# In[34]:

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


# In[35]:

class FreeozLinkSpider(scrapy.Spider):
    name = "FreeozLinkSpider"
    allowed_domains = ["www.freeoz.org"]
    start_urls = ['http://www.freeoz.org/ibbs/forum-7068-460.html']
    
    #this is how to initialize own's spider
    def __init__(self, *a, **kw):
        super(FreeozLinkSpider, self).__init__(*a, **kw)
        #link the spider cleaning signal with function
        dispatcher.connect(self.spider_closed, signals.spider_closed)
        
        #open('xxx.txt','a',0) open a file with unbuffered option which means text can be 
        #constantly written to file
        self.syd_file=open('sydney.link','a',0)
        self.mel_file=open('melbourne.link','a',0)
        self.act_file=open('canberra.link','a',0)
        self.per_file=open('perth.link','a',0)
        self.ade_file=open('adelaide.link','a',0)
        self.bne_file=open('brisbane.link','a',0)
        
    def spider_closed(self):
        self.syd_file.close()
        self.mel_file.close()
        self.bne_file.close()
        self.ade_file.close()
        self.per_file.close()
        self.act_file.close()
        
    def write_link_to_files(self,location,full_link):
        if location.encode('utf-8') == '悉尼':
            self.syd_file.write(full_link+'\n')
            return
        if location.encode('utf-8') == '墨尔本':
            self.mel_file.write(full_link+'\n')
            return
        if location.encode('utf-8') == '布里斯班':
            self.bne_file.write(full_link+'\n')
            return
        if location.encode('utf-8') == '阿德莱德':
            self.ade_file.write(full_link+'\n')
            return
        if location.encode('utf-8') == '佩斯':
            self.per_file.write(full_link+'\n')
            return
        if location.encode('utf-8') == '堪培拉':
            self.act_file.write(full_link+'\n')
            return
    

    def parse(self, response):
        next_page_tag=response.xpath('//a[@href and @class="nxt"]/@href')
        if next_page_tag != []:
            next_page_link=str(urllib.basejoin(response.url,next_page_tag.extract()[0]))
            yield Request(next_page_link,callback=self.parse)
        th_tags=response.xpath('//th[@class="new" or @class="lock"]')
        for th_tag in th_tags:
            location=th_tag.xpath('em/a/text()').extract()[0]
            link=th_tag.xpath('a[@onclick="atarget(this)"]/@href').extract()[0]
            full_link=urllib.basejoin(response.url,link)
            self.write_link_to_files(location,full_link)
            


# In[39]:

def main():
    result_queue = Queue()
    crawler = CrawlerWorker(FreeozLinkSpider(), result_queue)
    crawler.start()
    #in the spider output has already been written to local file
    #for item in result_queue.get():
        #print item
    
        


# In[ ]:

if __name__ == '__main__':
    main()


# In[ ]:

#when all the links are written to local file.In the shell, can run
# time cat canberra.link | parallel wget -P ./canberra {}
#fast download and roughly 200 files/minute

