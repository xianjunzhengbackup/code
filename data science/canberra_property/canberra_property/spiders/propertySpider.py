# -*- coding: utf-8 -*-
import scrapy
import urllib
import csv
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from scrapy import Request

class PropertyspiderSpider(scrapy.Spider):
    name = "propertySpider"
    allowed_domains = ["realestate.com.au/"]
    start_urls = (
        'http://www.realestate.com.au/buy/in-canberra+-+greater+region%2c+act%3b/list-1',
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
        next_tags=response.xpath('//a[@title="View the next page of results"]/@href')
        if next_tags:
            next_link=urllib.parse.urljoin('http://www.realestate.com.au',next_tags[0].extract())
            #yield Request(next_link,callback=self.parse,headers=self.header,dont_filter=True)
           
        property_tags=response.xpath('//article[contains(@class,"resultBody")]')
        if property_tags:
            for each_property in property_tags:
                price_tag=each_property.xpath('div[@class="listingInfo rui-clearfix"]/div[@class="propertyStats"]/p[@class="priceText" or @class="contactAgent"]/text()')
                if price_tag:
                    price=price_tag.extract()[0]
                else:
                    price_tag=each_property.xpath('aside/div[@class="listingInfo rui-clearfix"]/div[@class="propertyStats"]/p[@class="priceText" or @class="contactAgent"]/text()')
                    if price_tag:
                        price=price_tag.extract()[0]
                    else:
                        price='n/a'
                    
                type_tag=each_property.xpath('div[@class="listingInfo rui-clearfix"]/div[@class="propertyStats"]/p[@class="type"]/text()')
                if type_tag:
                    type_property=type_tag.extract()[0]
                else:
                    type_tag=each_property.xpath('aside/div[@class="listingInfo rui-clearfix"]/div[@class="propertyStats"]/p[@class=""]/text()')
                    if type_tag:
                        type_property=type_tag.extract()[0]
                    else:
                        type_property='n/a'
                    
                address_tag=each_property.xpath('div[@class="listingInfo rui-clearfix"]/div[@class="vcard"]/h2/a/text()')
                link_tag=each_property.xpath('div[@class="listingInfo rui-clearfix"]/div[@class="vcard"]/h2/a/@href')
                if address_tag:
                    address=address_tag.extract()[0]
                else:
                    address_tag=each_property.xpath('aside/div[@class="listingInfo rui-clearfix"]/div[@class="vcard"]/h2/a/text()')
                    if address_tag:
                        address=address_tag.extract()[0]
                    else:
                        address='n/a'
                        
                if link_tag:
                    link_address=urllib.parse.urljoin('http://www.realestate.com.au',link_tag.extract()[0])
                else:
                    link_tag=each_property.xpath('aside/div[@class="listingInfo rui-clearfix"]/div[@class="vcard"]/h2/a/@href')
                    if link_tag:
                        link_address=urllib.parse.urljoin('http://www.realestate.com.au',link_tag.extract()[0])
                    else:
                        link_address='n/a'
                        
                bed_tag=each_property.xpath('div[@class="listingInfo rui-clearfix"]/dl/dd[1]/text()')
                if bed_tag:
                    bed=bed_tag.extract()[0]
                else:
                    bed_tag=each_property.xpath('aside/div[@class="listingInfo rui-clearfix"]/dl/dd[1]/text()')
                    bed=bed_tag.extract()[0]
                
                car_tag=each_property.xpath('div[@class="listingInfo rui-clearfix"]/dl/dd[2]/text()')
                if car_tag:
                    car=car_tag.extract()[0]
                else:
                    car_tag=each_property.xpath('aside/div[@class="listingInfo rui-clearfix"]/dl/dd[2]/text()')
                    car=car_tag.extract()[0]
                    
                bath_tag=each_property.xpath('div[@class="listingInfo rui-clearfix"]/dl/dd[3]/text()')
                if bath_tag:
                    bath=bath_tag.extract()[0]
                else:
                    bath_tag=each_property.xpath('aside/div[@class="listingInfo rui-clearfix"]/dl/dd[3]/text()')
                    bath=bath_tag.extract()[0]
                
                self.writer.writerow((price,type_property,address,link_address,bed,bath,car,response.url))
                