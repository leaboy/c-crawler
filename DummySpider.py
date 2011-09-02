
'''
Example of Usage
'''

import common
from ccrawler import CCrawler, Request
from selector import HtmlSelector

import logging
logger = common.logger(name=__name__, filename='ccrawler.log', level=logging.DEBUG)

class DummySpider:
    start_urls = ['http://www.blueidea.com/photo/gallery/']
    #start_urls = ['http://disclosure.szse.cn/m/drgg000023.htm', 'http://disclosure.szse.cn/m/drgg000024.htm']
    #start_urls = ['http://www.baidu.com', 'http://www.google.com', 'http://www.google.hk']
    workers = 100
    timeout = 8

    def parse(self, response):
        hxs = HtmlSelector(response)
        '''
        Usage re
        '''
        '''
        itemlist = hxs.re('<td class=\'td10\'> .*?<\/td>')
        for item in itemlist:
            title = item.re('<a[^>]*[^>]*>(.*)[^<]*<\/a>')
            print title
        '''
        #'''
        itemlist = hxs.re('<tr class=\"(border|pagelight)\">.*?<td nowrap>(.*?)<\/td>')
        linkitem = itemlist.re('<a[^>]*href=\"([^\s\"]+)\"[^>]*>[^<]*<\/a>').Link()
        for item in linkitem:
            title = item.re('<td class="content"><strong>(.*?)</strong></td>').extract()
            print title
        '''
        for item in linkitem:
            print item
        '''
        #print type(linkitem)
        #.Link()
        #print linkitem

        '''
        for item in itemlist:
            title = item.re('<a[^>]*>(.*)[^<]*<\/a>').extract()
            link = item.re('<a[^>]*href=\"([^\s\"]+)\"[^>]*>[^<]*<\/a>').Link()
            if link:
                print link[0].base_url
        '''
        #'''

        '''
        Usage xpath
        '''
        '''
        itemlist = hxs.select('//tr[@class!="listTitle"]/td[@nowrap]')
        for item in itemlist:
            title = item.select('a/text()').extract()
            if title:
                print title
        '''
    def process_item(self, item):
        for i in item:
            print i

class a:
    pass


spider = DummySpider()
crawler = CCrawler(spider)
crawler.start()

