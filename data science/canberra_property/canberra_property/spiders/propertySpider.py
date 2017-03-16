# -*- coding: utf-8 -*-
import scrapy
import urllib
import csv
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from scrapy import Request
import re
import base64

class PropertyspiderSpider(scrapy.Spider):
    name = "propertySpider"
    allowed_domains = ["realestate.com.au/"]
    urls=(
        'https://www.realestate.com.au/sold/in-2601%3b/list-1',
        'https://www.realestate.com.au/sold/in-2602%3b/list-1',
        'https://www.realestate.com.au/sold/in-2603%3b/list-1',
        'https://www.realestate.com.au/sold/in-2604%3b/list-1',
        'https://www.realestate.com.au/sold/in-2605%3b/list-1',
        'https://www.realestate.com.au/sold/in-2606%3b/list-1',
        'https://www.realestate.com.au/sold/in-2607%3b/list-1',
        'https://www.realestate.com.au/sold/in-2609%3b/list-1',
        'https://www.realestate.com.au/sold/in-2610%3b/list-1',
        'https://www.realestate.com.au/sold/in-2611%3b/list-1',
        'https://www.realestate.com.au/sold/in-2612%3b/list-1',
        'https://www.realestate.com.au/sold/in-2613%3b/list-1',
        'https://www.realestate.com.au/sold/in-2614%3b/list-1',
        'https://www.realestate.com.au/sold/in-2615%3b/list-1',
        'https://www.realestate.com.au/sold/in-2900%3b/list-1',
        'https://www.realestate.com.au/sold/in-2901%3b/list-1',
        'https://www.realestate.com.au/sold/in-2902%3b/list-1',
        'https://www.realestate.com.au/sold/in-2903%3b/list-1',
        'https://www.realestate.com.au/sold/in-2904%3b/list-1',
        'https://www.realestate.com.au/sold/in-2905%3b/list-1',
        'https://www.realestate.com.au/sold/in-2906%3b/list-1',
        'https://www.realestate.com.au/sold/in-2907%3b/list-1',
        'https://www.realestate.com.au/sold/in-2909%3b/list-1',
        'https://www.realestate.com.au/sold/in-2910%3b/list-1',
        'https://www.realestate.com.au/sold/in-2911%3b/list-1',
        'https://www.realestate.com.au/sold/in-2912%3b/list-1',
        'https://www.realestate.com.au/sold/in-2913%3b/list-1',
        'https://www.realestate.com.au/sold/in-2914%3b/list-1',
        'https://www.realestate.com.au/sold/in-2915%3b/list-1')
    start_urls = (
        'https://www.realestate.com.au/sold/in-2600%3b/list-1',
        'https://www.realestate.com.au/sold/in-2601%3b/list-1',
        'https://www.realestate.com.au/sold/in-2602%3b/list-1',
        'https://www.realestate.com.au/sold/in-2603%3b/list-1',
        'https://www.realestate.com.au/sold/in-2604%3b/list-1',
        'https://www.realestate.com.au/sold/in-2605%3b/list-1',
        'https://www.realestate.com.au/sold/in-2606%3b/list-1',
        'https://www.realestate.com.au/sold/in-2607%3b/list-1',
        'https://www.realestate.com.au/sold/in-2609%3b/list-1',
        'https://www.realestate.com.au/sold/in-2610%3b/list-1',
        'https://www.realestate.com.au/sold/in-2611%3b/list-1',
        'https://www.realestate.com.au/sold/in-2612%3b/list-1',
        'https://www.realestate.com.au/sold/in-2613%3b/list-1',
        'https://www.realestate.com.au/sold/in-2614%3b/list-1',
        'https://www.realestate.com.au/sold/in-2615%3b/list-1',
        'https://www.realestate.com.au/sold/in-2900%3b/list-1',
        'https://www.realestate.com.au/sold/in-2901%3b/list-1',
        'https://www.realestate.com.au/sold/in-2902%3b/list-1',
        'https://www.realestate.com.au/sold/in-2903%3b/list-1',
        'https://www.realestate.com.au/sold/in-2904%3b/list-1',
        'https://www.realestate.com.au/sold/in-2905%3b/list-1',
        'https://www.realestate.com.au/sold/in-2906%3b/list-1',
        'https://www.realestate.com.au/sold/in-2907%3b/list-1',
        'https://www.realestate.com.au/sold/in-2909%3b/list-1',
        'https://www.realestate.com.au/sold/in-2910%3b/list-1',
        'https://www.realestate.com.au/sold/in-2911%3b/list-1',
        'https://www.realestate.com.au/sold/in-2912%3b/list-1',
        'https://www.realestate.com.au/sold/in-2913%3b/list-1',
        'https://www.realestate.com.au/sold/in-2914%3b/list-1',
        'https://www.realestate.com.au/sold/in-2915%3b/list-1'
    )
    def __init__(self, *a, **kw):
        super(PropertyspiderSpider, self).__init__(*a, **kw)
        #link the spider cleaning signal with function
        dispatcher.connect(self.spider_closed, signals.spider_closed)
        self.fp=open('/home/jun_gentoo/git/code/data science/canberra_property/output.csv','w')
        self.writer=csv.writer(self.fp)
        self.header={}
        #self.header['Connection']='keep-alive'
        self.header['Accept']="text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
        self.header['Accept-Encoding']="gzip, deflate, sdch"
        self.header['Accept-Language']="en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2,ja;q=0.2"
        #self.header['Host']='http://www.google.com.au'
        #self.header['Upgrade-Insecure-Requests']='1'
        self.header['Referer']='https://www.google.com.au'
        self.header['User-Agent']="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.100 Safari/537.36"
        
    def spider_closed(self):
        if self.fp:
            self.fp.close()
    
    def parse(self, response):
        next_tags=response.xpath('//a[@title="Go to Next Page"]/@href')
        if next_tags:
            next_link=urllib.parse.urljoin('http://www.realestate.com.au',next_tags[0].extract())
            yield Request(next_link,callback=self.parse,headers=self.header,dont_filter=True)
           
        property_tags=response.xpath('//article[contains(@class,"results-card property-card")]')
        if property_tags:
            for each_property in property_tags:
                price_tag=each_property.xpath('div[contains(@class,"wrapper")]/div[contains(@class,"property-card__content")]/div[contains(@class,"price")]/span/text()')
                if price_tag:
                    price=price_tag.extract()[0]
                else:
                    price_tag=each_property.xpath('div[contains(@class,"wrapper")]/div[contains(@class,"property-card__content")]/div[contains(@class,"price")]/span/img/@src')
                    if price_tag:
                        price=price_tag.extract()[0]
                        pattern=re.compile(r'(?:convert\/)(.*)(?:\?font-family)')
                        price=pattern.search(price).groups()[0]
                        price=base64.b64decode(price)
                    else:
                        price='n/a'
                        
                address_tag=each_property.xpath('div[contains(@class,"wrapper")]/div[contains(@class,"property-card__content")]/div[contains(@class,"property-card__info")]/a[@class="property-card__info-text"]/span[1]/text()')
                if address_tag:
                    address=address_tag.extract()[0]
                else:
                    address='n/a'
                    
                suburb_tag=each_property.xpath('div[contains(@class,"wrapper")]/div[contains(@class,"property-card__content")]/div[contains(@class,"property-card__info")]/a[@class="property-card__info-text"]/span[2]/text()')
                if suburb_tag:
                    suburb=suburb_tag.extract()[0]
                else:
                    suburb='n/a'
                    
                property_type_tag=each_property.xpath('div[contains(@class,"wrapper")]/div[contains(@class,"property-card__content")]/div[contains(@class,"property-card__info")]/p/span[1]/text()')
                if property_type_tag:
                    property_type=property_type_tag.extract()[0]
                else:
                    property_type='n/a'
                    
                sold_date_tag=each_property.xpath('div[contains(@class,"wrapper")]/div[contains(@class,"property-card__content")]/div[contains(@class,"property-card__info")]/p/span[2]/child::node()')
                if sold_date_tag:
                    sold_date=sold_date_tag.extract()[-2]
                else:
                    sold_date='n/a'
                    
                bed_tag=each_property.xpath('div[contains(@class,"wrapper")]/div[contains(@class,"property-card__content")]/div[contains(@class,"property-card__general-features")]/ul/li[1]/span/child::node()')
                if bed_tag:
                    bed=bed_tag.extract()[-2]
                else:
                    bed='n/a'
                    
                bath_tag=each_property.xpath('div[contains(@class,"wrapper")]/div[contains(@class,"property-card__content")]/div[contains(@class,"property-card__general-features")]/ul/li[2]/span/child::node()')
                if bath_tag:
                    bath=bath_tag.extract()[-2]
                else:
                    bath='n/a'
                    
                car_tag=each_property.xpath('div[contains(@class,"wrapper")]/div[contains(@class,"property-card__content")]/div[contains(@class,"property-card__general-features")]/ul/li[3]/span/child::node()')
                if car_tag:
                    car=car_tag.extract()[-2]
                else:
                    car='n/a'
                    
                link_tag=each_property.xpath('a[@class="property-card__link"]/@href')
                if link_tag:
                    link=link_tag.extract()[0]
                    link=urllib.parse.urljoin('http://www.realestate.com.au',link)
                else:
                    link='n/a'
                refer=response.url
                self.writer.writerow((price,address,suburb,property_type,sold_date,bed,bath,car,link,refer))
                #print(price,address,suburb,sold_date,property_type,bed,bath,car,link)
                
