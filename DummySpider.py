# -*- coding: utf-8 -*-
'''
Example of Usage
'''

import common
from ccrawler import CCrawler
from selector import HtmlSelector

import logging
logger = common.logger(name=__name__, filename='ccrawler.log', level=logging.DEBUG)

class DummySpider:
    start_urls = ['http://disclosure.szse.cn/m/drgg000023.htm', 'http://disclosure.szse.cn/m/drgg000024.htm']
    workers = 100
    timeout = 8

    def parse(self, response):
        hxs = HtmlSelector(response.body)
        itemlist = hxs.select('//td[@class="td10"]')
        for item in itemlist:
            title = item.select('a/text()')
            #link = item.select('a/@href')
            #print item

    def process_item(self, item):
        pass

class a:
    pass


spider = DummySpider()
crawler = CCrawler(spider)
crawler.start()
crawler.stop()

'''
spider2 = a()
crawler2 = CCrawler('')
crawler2.start()
'''

