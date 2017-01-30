
# coding: utf-8

# In[147]:

from scrapy import signals
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess
from scrapy.xlib.pydispatch import dispatcher
from multiprocessing.queues import Queue
import scrapy
import multiprocessing
import urllib
from scrapy import Request as Request


# In[148]:

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


# In[149]:

class TigtagLinkSpider(scrapy.Spider):
    name = "TigtagLinkSpider"
    allowed_domains = ["tigtag.com"]
    start_urls = ['http://bbs.tigtag.com/forum.php?mod=forumdisplay&fid=48&typeid=201&filter=typeid&typeid=201&page=1']
    #start_urls = ['http://httpbin.org/headers']
    #allowed_domains=['httpbin.org']
    header={}
    #this is how to initialize own's spider
    def __init__(self, *a, **kw):
        super(TigtagLinkSpider, self).__init__(*a, **kw)
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
        
        #self.header['Connection']='keep-alive'
        self.header['Accept']="text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
        self.header['Accept-Encoding']="gzip, deflate, sdch"
        self.header['Accept-Language']="en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2,ja;q=0.2"
        #self.header['Host']='http://www.google.com.au'
        #self.header['Upgrade-Insecure-Requests']='1'
        self.header['Referer']='https://www.google.com.au'
        self.header['User-Agent']="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.100 Safari/537.36"
        
        
    def start_requests(self):
        for url in self.start_urls:
            yield Request(url=url,callback=self.parse,headers=self.header)
        
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
        #print("%s"%self.settings.attributes)
        #print response.body
        next_page_tag=response.xpath('//a[@href and @class="nxt"]/@href')
        if next_page_tag != []:
            tbody_tags=response.xpath('//tbody[contains(@id,"normalthread_")]')
            for tbody in tbody_tags:
                location=tbody.xpath('tr/td/div/div/span/em/a/text()').extract()[0]
                link=tbody.xpath('tr/td/div/div/a[@href and @class="td_link_title"]/@href').extract()[0]
                self.write_link_to_files(location,link)
            next_page_link=str(urllib.basejoin(response.url,next_page_tag.extract()[0]))
            print next_page_link
            yield Request(url=next_page_link,callback=self.parse,headers=self.header)
        #    pass
            


# In[150]:

def main():
    result_queue = Queue()
    crawler = CrawlerWorker(TigtagLinkSpider(), result_queue)
    crawler.start()
    #in the spider output has already been written to local file
    #for item in result_queue.get():
        #print item


# In[151]:

if __name__ == '__main__':
    main()


# In[ ]:



